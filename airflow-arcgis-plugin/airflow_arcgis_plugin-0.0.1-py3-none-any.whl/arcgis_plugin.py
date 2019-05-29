# Plugin definition file.
from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator
from airflow.hooks.base_hook import BaseHook
from airflow_arcgis.operators.arcgis_operator import PostgresToArcGISOperator
from airflow_arcgis.hooks.arcgis_hook import ArcGISHook


class ArcGISPlugin(AirflowPlugin):
    name = "airflow_arcgis"
    operators = [PostgresToArcGISOperator]
    hooks = [ArcGISHook]

    # A list of class(es) derived from BaseExecutor
    executors = []
    # A list of references to inject into the macros namespace
    macros = []
    # A list of objects created from a class derived
    # from flask_admin.BaseView
    admin_views = []
    # A list of Blueprint object created from flask.Blueprint
    flask_blueprints = []
    # A list of menu links (flask_admin.base.MenuLink)
    menu_links = []
