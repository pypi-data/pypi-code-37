import datetime

from yaml import dump

from airflow import DAG

from dagster import check, PipelineDefinition
from dagster.core.execution import create_execution_plan
from dagster.utils.indenting_printer import IndentingStringIoPrinter

from .operators import DagsterDockerOperator, DagsterOperator, DagsterPythonOperator
from .compile import coalesce_execution_steps


DEFAULT_ARGS = {
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': datetime.timedelta(0, 300),
    'start_date': datetime.datetime(1900, 1, 1, 0, 0),
}


def _make_dag_description(pipeline_name, env_config):
    with IndentingStringIoPrinter() as printer:
        printer.block(
            '\'\'\'Editable scaffolding autogenerated by dagster-airflow from pipeline '
            '{pipeline_name} with config:'.format(pipeline_name=pipeline_name)
        )
        printer.blank_line()

        with printer.with_indent():
            for line in dump(env_config).split('\n'):
                printer.line(line)
        printer.blank_line()

        return printer.read()


def _make_airflow_dag(
    pipeline,
    env_config=None,
    dag_id=None,
    dag_description=None,
    dag_kwargs=None,
    op_kwargs=None,
    operator=DagsterPythonOperator,
):

    check.inst_param(pipeline, 'pipeline', PipelineDefinition)
    env_config = check.opt_dict_param(env_config, 'env_config', key_type=str)
    pipeline_name = pipeline.name
    dag_id = check.opt_str_param(dag_id, 'dag_id', pipeline.name)
    dag_description = check.opt_str_param(
        dag_description, 'dag_description', _make_dag_description(pipeline_name, env_config)
    )
    check.subclass_param(operator, 'operator', DagsterOperator)
    # black 18.9b0 doesn't support py27-compatible formatting of the below invocation (omitting
    # the trailing comma after **check.opt_dict_param...) -- black 19.3b0 supports multiple python
    # versions, but currently doesn't know what to do with from __future__ import print_function --
    # see https://github.com/ambv/black/issues/768
    # fmt: off
    dag_kwargs = dict(
        {'default_args': DEFAULT_ARGS},
        **check.opt_dict_param(dag_kwargs, 'dag_kwargs', key_type=str)
    )
    # fmt: on

    op_kwargs = check.opt_dict_param(op_kwargs, 'op_kwargs', key_type=str)

    dag = DAG(dag_id=dag_id, description=dag_description, **dag_kwargs)

    execution_plan = create_execution_plan(pipeline, env_config)

    tasks = {}

    coalesced_plan = coalesce_execution_steps(execution_plan)

    for solid_name, solid_steps in coalesced_plan.items():

        step_keys = [step.key for step in solid_steps]

        task = operator.operator_for_solid(
            pipeline=pipeline,
            env_config=env_config,
            solid_name=solid_name,
            step_keys=step_keys,
            dag=dag,
            dag_id=dag_id,
            op_kwargs=op_kwargs,
        )

        tasks[solid_name] = task

        for solid_step in solid_steps:
            for step_input in solid_step.step_inputs:
                prev_solid_name = execution_plan.get_step_by_key(
                    step_input.prev_output_handle.step_key
                ).solid_name
                if solid_name != prev_solid_name:
                    tasks[prev_solid_name].set_downstream(task)

    return (dag, [tasks[solid_name] for solid_name in coalesced_plan.keys()])


def make_airflow_dag(
    pipeline, env_config=None, dag_id=None, dag_description=None, dag_kwargs=None, op_kwargs=None
):
    return _make_airflow_dag(
        pipeline=pipeline,
        env_config=env_config,
        dag_id=dag_id,
        dag_description=dag_description,
        dag_kwargs=dag_kwargs,
        op_kwargs=op_kwargs,
    )


def make_airflow_dag_containerized(
    pipeline,
    image,
    env_config=None,
    dag_id=None,
    dag_description=None,
    dag_kwargs=None,
    op_kwargs=None,
):
    op_kwargs = check.opt_dict_param(op_kwargs, 'op_kwargs', key_type=str)
    op_kwargs['image'] = image
    return _make_airflow_dag(
        pipeline=pipeline,
        env_config=env_config,
        dag_id=dag_id,
        dag_description=dag_description,
        dag_kwargs=dag_kwargs,
        op_kwargs=op_kwargs,
        operator=DagsterDockerOperator,
    )
