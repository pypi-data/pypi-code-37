# Operators used to inteface with ArcGIS.
from arcgis.features import Feature, FeatureLayer

from airflow.models import BaseOperator
from airflow.models import Connection
from airflow.exceptions import AirflowException

from airflow.hooks.postgres_hook import PostgresHook
from airflow_arcgis.hooks.arcgis_hook import ArcGISHook


DEFAULT_PG_CONN = "etl_postgres"
DEFAULT_PG_DB = "etl"
DEFAULT_PG_SCHEMA = "public"
UPLOAD_CHUNK_SIZE = 1000


class ArcGISOperator(BaseOperator):
    """The base ArcGIS operator.
    """

    def __init__(self, *args, **kwargs):
        """Initializes a base ArcGIS operator.
        """

        # Set alternative connection ID if specified
        self.conn_id = None
        if "conn_id" in kwargs:
            cid_value = kwargs["conn_id"]
            if type(cid_value) is str:
                self.conn_id = cid_value

        super().__init__(*args, **kwargs)

    def execute(self, **kwargs):
        """Creates a ArcGIS hook and establishes connection.

        Arguments:
            context {[type]} -- [description]
        """

        self.arcgis = ArcGISHook(self.conn_id).get_conn()


class PostgresToArcGISOperator(ArcGISOperator):
    """The ArcGIS operator to sync feature layers with PostgreSQL views.
    """

    def __init__(self,
                 view_name,
                 feature_layer_id,
                 postgres_conn_id=None,
                 postgres_database=None,
                 postgres_schema=None,
                 no_diff=False,
                 *args, **kwargs):
        """Initializes an ArcGIS Sync operator.

        Arguments:
            view_name {str} -- The name of the source PostgreSQL view.
            feature_layer_id {int} -- The ID of the target ArcGIS feature layer.

        Keyword Arguments:
            no_diff {bool} -- Whether to disable incremental update. (default: {False})
        """

        self.view_name = view_name
        self.feature_layer_id = feature_layer_id
        self.postgres_conn_id = postgres_conn_id
        self.postgres_database = postgres_database
        self.postgres_schema = postgres_schema
        self.no_diff = no_diff

        if postgres_conn_id is None:
            self.postgres_conn_id = DEFAULT_PG_CONN

        if postgres_database is None:
            self.postgres_database = DEFAULT_PG_DB

        if postgres_schema is None:
            self.postgres_schema = DEFAULT_PG_SCHEMA

        super().__init__(*args, **kwargs)

    def _select_view(self):
        """Selects the view from PostgreSQL database.

        Returns:
            list -- Query results.
        """

        return self.postgres.execute(f"SELECT * FROM {self.view_name};")
    
    def _fetch_fields(self):
        """Selects one row from the table and extracts all field names.
        """

        row = self.postgres.execute(f"SELECT * FROM {self.view_name} LIMIT 1;")
        self.fields = row.keys()

    def _fetch_db(self):
        """Fetches old and new view snapshots from the database.

        Returns:
            tuple -- The old view and the new view.
        """

        old_view = None
        if not self.no_diff:
            old_view = self._select_view()
            self.postgres.execute(f"REFRESH MATERIALIZED VIEW {self.view_name};")
        
        new_view = self._select_view()
        return old_view, new_view

    def _get_oid_key(self):
        """Gets the name of the ObjectID field in the current feature layer.

        Raises:
            AirflowException: Raised when a field of type OID is not found.

        Returns:
            str -- The name of the OID field.
        """

        fl_fields = self.feature_layer.properties["fields"]
        oid_field = [field["type"] ==
                     "esriFieldTypeOID" for field in fl_fields]
        if oid_field is None:
            raise AirflowException(
                "No field of type OID is found in the feature layer.")

        return oid_field["name"]

    def _truncate_feature_layer(self):
        """Truncate (drop) the feature layer.
        Here be dragons!
        """

        result = self.feature_layer.manager.truncate()
        if not result["success"]:
            raise AirflowException("Failed truncating the feature layer.")

    def _push_table(self):
        """Constructs a dict-styled list from database records and push it to ArcGIS.
        """

        payload = [{ "attributes": dict(zip(self.fields, record)) } for record in self.new_view]

        # Code from etl-airflow
        for i in range(0, len(payload), UPLOAD_CHUNK_SIZE):
            try:
                self.feature_layer.edit_features(
                    adds=payload[i:i + UPLOAD_CHUNK_SIZE])
            except:
                print(f"Errored on {i} - splitting into 2 batches")

                start = i
                middle = int(i + (UPLOAD_CHUNK_SIZE / 2))
                end = i + UPLOAD_CHUNK_SIZE

                self.feature_layer.edit_features(adds=payload[start:middle])
                self.feature_layer.edit_features(adds=payload[middle:end])

    def _push_diff(self):
        """Removes stale rows from ArcGIS and adds fresh rows.
        """

        deltas = self.new_view - self.old_view
        stales = self.old_view - self.new_view

        # Drop all stales
        stale_ids = [stale[self.oid_key] for stale in stales]
        self.feature_layer.edit_features(deletes=stale_ids)

        # Push all deltas
        delta_features = [Feature.from_dict(dict(zip(self.fields, new_row)))
                      for new_row in self.new_view]
        self.feature_layer.edit_features(adds=delta_features)

    def execute(self, context=None):
        """Syncs the specified feature set with the specified PostgreSQL view.

        Arguments:
            context {[type]} -- [description]
        """

        # Initialize PostgreSQL hook
        self.postgres = PostgresHook(
            postgres_conn_id=self.postgres_conn_id,
            schema=self.postgres_database).get_sqlalchemy_engine()

        # Initialize ArcGIS hook
        super().execute()
        fl_item = self.arcgis.content.get(self.feature_layer_id)
        fl_url = fl_item.layers[0].url
        self.feature_layer = FeatureLayer(fl_url)

        # Load views
        self._fetch_fields()
        self.old_view, self.new_view = self._fetch_db()

        if self.no_diff:
            # Push the whole table
            self._truncate_feature_layer()
            self._push_table()
        else:
            # Push differences
            # self.oid_key = self._get_oid_key()
            self.fields = self.postgres.keys()
            self.oid_key = self.fields[0];
            self._push_diff()
