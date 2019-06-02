# -*- coding: utf-8 -*-
"""Base class for handling storage operations like saving and loading."""
import abc
from pathlib import Path
from glcs import (course, student, assignment,
                  projectsettings, credentials, instructor)
import logging
from xdg import (XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME)


class StorageManager(abc.ABC):
    """Abstract class to create an interface for saving and loading objects."""

    @abc.abstractmethod
    def save(self, obj):
        pass

    @abc.abstractmethod
    def load(self, obj, obj_info):
        pass


class FileManager(StorageManager):
    """Creates a storage manager which stores objects in files.

    Implements the StorageManager interface."""

    def __init__(self, logging_level=logging.INFO):
        log_format = "%(levelname)s:glcs.storage.FileManager%(message)s"
        logging.basicConfig(format=log_format, level=logging_level)

        self.home['data'] = XDG_DATA_HOME / "glcs"
        self.home['config'] = XDG_CONFIG_HOME / "glcs"
        self.home['cache'] = XDG_CACHE_HOME / "glcs"

        if not Path(self.home['data']).exist():
            logging.info(str(self.home['data']) + " not found, creating")
            Path(self.home['data']).mkdir()

        if not Path(self.home['config']).exist():
            logging.info(str(self.home['config']) + " not found, creating")
            Path(self.home['config']).mkdir()

        if not Path(self.home['cache']).exist():
            logging.info(str(self.home['cache']) + " not found, creating")
            Path(self.home['cache']).mkdir()

    def save(self, obj):
        if isinstance(obj, course.Course):
            self.__saveCourse(obj)
        elif isinstance(obj, student.Student):
            self.__saveStudent(obj)
        elif isinstance(obj, assignment.Assignment):
            self.__saveAssignment(obj)
        elif isinstance(obj, instructor.Instructor):
            self.__saveInstructor(obj)
        elif isinstance(obj, credentials.Credentials):
            self.__saveCredentials(obj)
        elif isinstance(obj, projectsettings.ProjectSettings):
            self.__saveProjectSettigns(obj)

    def __saveCourse(self, course):
        pass

    def __saveStudent(self, student):
        pass

    def __saveAssignment(self, assignment):
        pass

    def __saveInstructor(self, instructor):
        pass

    def __saveCredentials(self, credentials):
        pass

    def __saveProjectSettings(self, settings):
        pass

    def load(self, obj, obj_info):
        pass


class DatabaseManager(StorageManager):
    """Creates a storage manager which stores objects in a database.

    Implements the StorageManager interface."""

    def save(self, obj):
        pass

    def load(self, obj, obj_info):
        pass
