# Hooks used to interface with ArcGIS.
from arcgis.gis import GIS

from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable
from airflow.exceptions import AirflowException


DEFAULT_AGO_CONN = "http_ago"

class ArcGISHook(BaseHook):
    """Interact with ArcGIS using ArcGIS's Python SDK.
    """

    def __init__(self, conn_id=None):
        """Initializes the hook with ArcGIS SDK.
        
        Keyword Arguments:
            conn_id {str} -- Name of alternative connection to be used. (default: {None})
        """
        
        self.conn_info = self.__get_conn_info(conn_id)
    
    def __get_conn_info(self, conn_id=None):
        """Retrieves connection info from Airflow connections.
        
        Keyword Arguments:
            conn_id {str} -- Name of alternative connection to be used. (default: {None})
        
        Returns:
            Connection -- Connection info for ArcGIS.
        """

        if conn_id is not None:
            # Use overrride conn ID
            return self.get_connection(conn_id)
        else:
            return self.get_connection(DEFAULT_AGO_CONN)
    
    def get_conn(self):
        """Authenticates with the ArcGIS API and returns the session object.
        """

        return GIS(
            self.conn_info.host,
            self.conn_info.login,
            self.conn_info.password)
