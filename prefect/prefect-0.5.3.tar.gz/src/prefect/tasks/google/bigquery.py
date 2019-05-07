import uuid
from typing import List

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.oauth2.service_account import Credentials

from prefect import context
from prefect.client import Secret
from prefect.core import Task
from prefect.engine.signals import SUCCESS
from prefect.utilities.tasks import defaults_from_attrs


class BigQueryTask(Task):
    """
    Task for executing queries against a Google BigQuery table and (optionally) returning
    the results.  Note that _all_ initialization settings can be provided / overwritten at runtime.

    Args:
        - query (str, optional): a string of the query to execute
        - query_params (list[tuple], optional): a list of 3-tuples specifying
            BigQuery query parameters; currently only scalar query parameters are supported. See
            [the Google documentation](https://cloud.google.com/bigquery/docs/parameterized-queries#bigquery-query-params-python)
            for more details on how both the query and the query parameters should be formatted
        - project (str, optional): the project to initialize the BigQuery Client with; if not provided,
            will default to the one inferred from your credentials
        - location (str, optional): location of the dataset which will be queried; defaults to "US"
        - dry_run_max_bytes (int, optional): if provided, the maximum number of bytes the query is allowed
            to process; this will be determined by executing a dry run and raising a `ValueError` if the
            maximum is exceeded
        - credentials_secret (str, optional): the name of the Prefect Secret containing a JSON representation
            of your Google Application credentials; defaults to `"GOOGLE_APPLICATION_CREDENTIALS"`
        - dataset_dest (str, optional): the optional name of a destination dataset to write the
            query results to, if you don't want them returned; if provided, `table_dest` must also be
            provided
        - table_dest (str, optional): the optional name of a destination table to write the
            query results to, if you don't want them returned; if provided, `dataset_dest` must also be
            provided
        - job_config (dict, optional): an optional dictionary of job configuration parameters; note that
            the parameters provided here must be pickleable (e.g., dataset references will be rejected)
        - **kwargs (optional): additional kwargs to pass to the `Task` constructor
    """

    def __init__(
        self,
        query: str = None,
        query_params: List[tuple] = None,  # 3-tuples
        project: str = None,
        location: str = "US",
        dry_run_max_bytes: int = None,
        credentials_secret: str = None,
        dataset_dest: str = None,
        table_dest: str = None,
        job_config: dict = None,
        **kwargs
    ):
        self.query = query
        self.query_params = query_params
        self.project = project
        self.location = location
        self.dry_run_max_bytes = dry_run_max_bytes
        self.credentials_secret = credentials_secret or "GOOGLE_APPLICATION_CREDENTIALS"
        self.dataset_dest = dataset_dest
        self.table_dest = table_dest
        self.job_config = job_config or {}
        super().__init__(**kwargs)

    @defaults_from_attrs(
        "query",
        "query_params",
        "project",
        "location",
        "dry_run_max_bytes",
        "credentials_secret",
        "dataset_dest",
        "table_dest",
        "job_config",
    )
    def run(
        self,
        query: str = None,
        query_params: List[tuple] = None,
        project: str = None,
        location: str = "US",
        dry_run_max_bytes: int = None,
        credentials_secret: str = None,
        dataset_dest: str = None,
        table_dest: str = None,
        job_config: dict = None,
    ):
        """
        Run method for this Task.  Invoked by _calling_ this Task within a Flow context, after initialization.

        Args:
            - query (str, optional): a string of the query to execute
            - query_params (list[tuple], optional): a list of 3-tuples specifying
                BigQuery query parameters; currently only scalar query parameters are supported. See
                [the Google documentation](https://cloud.google.com/bigquery/docs/parameterized-queries#bigquery-query-params-python)
                for more details on how both the query and the query parameters should be formatted
            - project (str, optional): the project to initialize the BigQuery Client with; if not provided,
                will default to the one inferred from your credentials
            - location (str, optional): location of the dataset which will be queried; defaults to "US"
            - dry_run_max_bytes (int, optional): if provided, the maximum number of bytes the query is allowed
                to process; this will be determined by executing a dry run and raising a `ValueError` if the
                maximum is exceeded
            - credentials_secret (str, optional): the name of the Prefect Secret containing a JSON representation
                of your Google Application credentials; defaults to `"GOOGLE_APPLICATION_CREDENTIALS"`
            - dataset_dest (str, optional): the optional name of a destination dataset to write the
                query results to, if you don't want them returned; if provided, `table_dest` must also be
                provided
            - table_dest (str, optional): the optional name of a destination table to write the
                query results to, if you don't want them returned; if provided, `dataset_dest` must also be
                provided
            - job_config (dict, optional): an optional dictionary of job configuration parameters; note that
                the parameters provided here must be pickleable (e.g., dataset references will be rejected)

        Raises:
            - ValueError: if the `query` is `None`
            - ValueError: if only one of `dataset_dest` / `table_dest` is provided
            - ValueError: if the query will execeed `dry_run_max_bytes`

        Returns:
            - list: a fully populated list of Query results, with one item per row
        """
        ## check for any argument inconsistencies
        if query is None:
            raise ValueError("No query provided.")
        if sum([dataset_dest is None, table_dest is None]) == 1:
            raise ValueError(
                "Both `dataset_dest` and `table_dest` must be provided if writing to a destination table."
            )

        ## create client
        creds = Secret(credentials_secret).get()
        credentials = Credentials.from_service_account_info(creds)
        project = project or credentials.project_id
        client = bigquery.Client(project=project, credentials=credentials)

        ## setup jobconfig
        job_config = bigquery.QueryJobConfig(**job_config)
        if query_params is not None:
            hydrated_params = [
                bigquery.ScalarQueryParameter(*qp) for qp in query_params
            ]
            job_config.query_parameters = hydrated_params

        ## perform dry_run if requested
        if dry_run_max_bytes is not None:
            old_info = dict(
                dry_run=job_config.dry_run, use_query_cache=job_config.use_query_cache
            )
            job_config.dry_run = True
            job_config.use_query_cache = False
            self.logger.debug("Performing a dry run...")
            query_job = client.query(query, location=location, job_config=job_config)
            if query_job.total_bytes_processed > dry_run_max_bytes:
                raise ValueError(
                    "Query will process {0} bytes which is above the set maximum of {1} for this task.".format(
                        query_job.total_bytes_processed, dry_run_max_bytes
                    )
                )
            job_config.dry_run = old_info["dry_run"]
            job_config.use_query_cache = old_info["use_query_cache"]

        ## if writing to a destination table
        if dataset_dest is not None:
            table_ref = client.dataset(dataset_dest).table(table_dest)
            job_config.destination = table_ref

        query_job = client.query(query, location=location, job_config=job_config)
        return list(query_job.result())


class BigQueryStreamingInsert(Task):
    """
    Task for insert records in a Google BigQuery table via [the streaming API](https://cloud.google.com/bigquery/streaming-data-into-bigquery).
    Note that all of these settings can optionally be provided or overwritten at runtime.

    Args:
        - dataset_id (str, optional): the id of a destination dataset to write the
            records to
        - table (str, optional): the name of a destination table to write the
            records to
        - project (str, optional): the project to initialize the BigQuery Client with; if not provided,
            will default to the one inferred from your credentials
        - location (str, optional): location of the dataset which will be queried; defaults to "US"
        - credentials_secret (str, optional): the name of the Prefect Secret containing a JSON representation
            of your Google Application credentials; defaults to `"GOOGLE_APPLICATION_CREDENTIALS"`
        - **kwargs (optional): additional kwargs to pass to the `Task` constructor
    """

    def __init__(
        self,
        dataset_id: str = None,
        table: str = None,
        project: str = None,
        location: str = "US",
        credentials_secret: str = None,
        **kwargs
    ):
        self.dataset_id = dataset_id
        self.table = table
        self.project = project
        self.location = location
        self.credentials_secret = credentials_secret or "GOOGLE_APPLICATION_CREDENTIALS"
        super().__init__(**kwargs)

    @defaults_from_attrs(
        "dataset_id", "table", "project", "location", "credentials_secret"
    )
    def run(
        self,
        records: List[dict],
        dataset_id: str = None,
        table: str = None,
        project: str = None,
        location: str = "US",
        credentials_secret: str = None,
        **kwargs
    ):
        """
        Run method for this Task.  Invoked by _calling_ this Task within a Flow context, after initialization.

        Args:
            - records (list[dict]): the list of records to insert as rows into
                the BigQuery table; each item in the list should be a dictionary whose keys correspond
                to columns in the table
            - dataset_id (str, optional): the id of a destination dataset to write the
                records to; if not provided here, will default to the one provided at initialization
            - table (str, optional): the name of a destination table to write the
                records to; if not provided here, will default to the one provided at initialization
            - project (str, optional): the project to initialize the BigQuery Client with; if not provided,
                will default to the one inferred from your credentials
            - location (str, optional): location of the dataset which will be queried; defaults to "US"
            - credentials_secret (str, optional): the name of the Prefect Secret containing a JSON representation
                of your Google Application credentials; defaults to `"GOOGLE_APPLICATION_CREDENTIALS"`
            - **kwargs (optional): additional kwargs to pass to the
                `insert_rows_json` method; see the documentation here:
                https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.client.Client.html

        Raises:
            - ValueError: if all required arguments haven't been provided
            - ValueError: if any of the records result in errors

        Returns:
            - the response from `insert_rows_json`
        """
        ## check for any argument inconsistencies
        if dataset_id is None or table is None:
            raise ValueError("Both dataset_id and table must be provided.")

        ## create client
        creds = Secret(credentials_secret).get()
        credentials = Credentials.from_service_account_info(creds)
        project = project or credentials.project_id
        client = bigquery.Client(project=project, credentials=credentials)

        ## get table reference
        table_ref = client.dataset(dataset_id).table(table)

        ## stream data in
        response = client.insert_rows_json(table=table_ref, json_rows=records, **kwargs)

        errors = []
        output = []
        for row in response:
            output.append(row)
            if "errors" in row:
                errors.append(row["errors"])

        if errors:
            raise ValueError(errors)

        return output


class CreateBigQueryTable(Task):
    """
    Ensures a BigQuery table exists; creates it otherwise. Note that most initialization keywords
    can optionally be provided at runtime.

    Args:
        - project (str, optional): the project to initialize the BigQuery Client with; if not provided,
            will default to the one inferred from your credentials
        - credentials_secret (str, optional): the name of the Prefect Secret containing a JSON representation
            of your Google Application credentials; defaults to `"GOOGLE_APPLICATION_CREDENTIALS"`
        - dataset (str, optional): the name of a dataset in which the table will be created
        - table (str, optional): the name of a table to create
        - schema (List[bigquery.SchemaField], optional): the schema to use when creating the table
        - clustering_fields (List[str], optional): a list of fields to cluster the table by
        - time_partitioning (bigquery.TimePartitioning, optional): a `bigquery.TimePartitioning` object specifying
            a partitioninig of the newly created table
        - **kwargs (optional): additional kwargs to pass to the `Task` constructor
    """

    def __init__(
        self,
        project: str = None,
        credentials_secret: str = None,
        dataset: str = None,
        table: str = None,
        schema: List[bigquery.SchemaField] = None,
        clustering_fields: List[str] = None,
        time_partitioning: bigquery.TimePartitioning = None,
        **kwargs
    ):
        self.project = project
        self.credentials_secret = credentials_secret or "GOOGLE_APPLICATION_CREDENTIALS"
        self.dataset = dataset
        self.table = table
        self.schema = schema
        self.clustering_fields = clustering_fields
        self.time_partitioning = time_partitioning
        super().__init__(**kwargs)

    @defaults_from_attrs("project", "credentials_secret", "dataset", "table", "schema")
    def run(
        self,
        project: str = None,
        credentials_secret: str = None,
        dataset: str = None,
        table: str = None,
        schema: List[bigquery.SchemaField] = None,
    ):
        """
        Run method for this Task.  Invoked by _calling_ this Task within a Flow context, after initialization.

        Args:
            - project (str, optional): the project to initialize the BigQuery Client with; if not provided,
                will default to the one inferred from your credentials
            - credentials_secret (str, optional): the name of the Prefect Secret containing a JSON representation
                of your Google Application credentials; defaults to `"GOOGLE_APPLICATION_CREDENTIALS"`
            - dataset (str, optional): the name of a dataset in which the table will be created
            - table (str, optional): the name of a table to create
            - schema (List[bigquery.SchemaField], optional): the schema to use when creating the table

        Returns:
            - None

        Raises:
            - SUCCESS: a `SUCCESS` signal if the table already exists
        """
        creds = Secret(credentials_secret).get()
        credentials = Credentials.from_service_account_info(creds)
        project = project or credentials.project_id
        client = bigquery.Client(project=project, credentials=credentials)

        try:
            dataset_ref = client.get_dataset(dataset)
        except NotFound:
            self.logger.debug("Dataset {} not found, creating...".format(dataset))
            dataset_ref = client.create_dataset(dataset)

        table_ref = dataset_ref.table(table)
        try:
            client.get_table(table_ref)
            raise SUCCESS(
                "{dataset}.{table} already exists.".format(dataset=dataset, table=table)
            )
        except NotFound:
            self.logger.debug("Table {} not found, creating...".format(table))
            table = bigquery.Table(table_ref, schema=schema)

            # partitioning
            if self.time_partitioning:
                table.time_partitioning = self.time_partitioning

            # cluster for optimal data sorting/access
            if self.clustering_fields:
                table.clustering_fields = self.clustering_fields
            client.create_table(table)
