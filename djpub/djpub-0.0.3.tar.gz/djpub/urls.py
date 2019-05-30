# -*- coding: utf-8 -*-

"""URL related functions and classes

-------------------------------------------------------------------
Copyright: Md. Jahidul Hamid <jahidulhamid@yahoo.com>

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
-------------------------------------------------------------------
"""


import os
import glob
import logging
from django.urls import path
from django.utils.module_loading import import_string
from django.conf import settings as S


logging.basicConfig(
    level = logging.DEBUG if S.DEBUG else logging.INFO,
    format = '%(levelname)s:%(name)s: %(message)s',
)
logger = logging.getLogger(__name__)


DJPUB_VIEW_DIR_NAME = 'djpub_view'


class UrlPatterns(object):
    """Class to be inherited by djpub UrlPatterns in djpub_view
    
    Provides a get_urlpatterns() method which is called to get the url patterns.
    """

    current_djpub_view_dotted_path = '' # do not modify this variable in subclasses, only use

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def get_urlpatterns(self):
        """Return the url_patterns list that will be handled by the corresponding views

        Raises:
            NotImplementedError: This method must be implemented

        Returns:
            list: Should return a list of django URLPatterns
        """
        raise NotImplementedError(f"This method '{UrlPatterns.get_urlpatterns.__name__}' must be overriden in {self._get_current_djpub_view_dotted_path()}.{self.__class__.__name__}")
    
    def _get_urlpatterns(self):
        """Internal method. Do not override.

        Returns:
            list: List of django URLPatterns
        """
        return self.get_urlpatterns()
    
    def get_desired_position_index(self):
        """Return the desired position index where these url patterns should be inserted.
        
        0 will try to add these urlpatterns at the beginning.

        Multiple djpub_views using the same index will stay together but the order is not strictly defined.
        
        With current implementation the order is reverse alphabetic for same index patterns - [30/05/2019].
        
        Raises:
            NotImplementedError: This method must be implemented
        
        Returns:
            (int): A number designating the desired postion where these urlpatterns need to be inserted.
        """
        raise NotImplementedError(f"This method '{UrlPatterns.get_desired_position_index.__name__}' must be overriden in {self._get_current_djpub_view_dotted_path()}.{self.__class__.__name__}")
    
    def _get_desired_position_index(self):
        """Internal method. Do not override.
        
        Raises exception for invalid index
        
        Returns:
            int: position index
        """
        index = self.get_desired_position_index()
        if not isinstance(index, int):
            raise ValueError(f"Expected a int value from {self._get_current_djpub_view_dotted_path()}.{self.__class__.__name__}.{UrlPatterns.get_desired_position_index.__name__}, but {type(index)} is provided")
        if index < 0:
            raise ValueError(f"Position index can not be less than 0 in {self._get_current_djpub_view_dotted_path()}.{self.__class__.__name__}.{UrlPatterns.get_desired_position_index.__name__}")
        return index

    def get_current_djpub_view_dotted_path(self):
        """Return current_djpub_view_dotted_path if exists, otherwise None

        Do not override this method in subclasses.
        
        Returns:
            str: current djpub view dotted path or None
        """
        return self.current_djpub_view_dotted_path

    def _get_current_djpub_view_dotted_path(self):
        current_djpub_view_dotted_path = self.get_current_djpub_view_dotted_path()
        return current_djpub_view_dotted_path if current_djpub_view_dotted_path else '[current_djpub_view_dotted_path]'



def get_urlpatterns(djpub_view_search_paths, project_root_dir):
    """Search all djpub views and return a urlpattern list
    
    Args:
        djpub_view_search_paths (list): A list of paths where we will search for DJPUB views.
        project_root_dir (str): The django project root directory from where import starts, e.g project.app means we need the parent of project package.
    """
    logger.debug(f"Starting search for djpub_views in {str(djpub_view_search_paths)}")
    urlpatterns = []
    for path in djpub_view_search_paths:
        logger.debug(f"Searching for djpub_view in {path}")
        for parent, folders, files in os.walk(path):
            for folder in folders:
                if folder == DJPUB_VIEW_DIR_NAME:
                    folder = os.path.join(parent, folder)
                    logger.debug(f"djpub view dir: {folder}")
                    view_package_path = folder.replace(project_root_dir, '').strip(os.path.sep).replace(os.path.sep, '.')
                    logger.debug(f"view_package_path: {view_package_path}")
                    _URLPatterns_Class = import_string(f"{view_package_path}.{UrlPatterns.__name__}")
                    _URLPatterns = _URLPatterns_Class(current_djpub_view_dotted_path=view_package_path)
                    _urlpatterns = _URLPatterns._get_urlpatterns()
                    logger.debug(f"UrlPatterns.get_urlpatterns(): {str(_urlpatterns)}")
                    _position = _URLPatterns._get_desired_position_index()
                    urlpatterns[_position:_position] = _urlpatterns
    logger.debug(f"urlpatterns: {str(urlpatterns)}")
    return urlpatterns