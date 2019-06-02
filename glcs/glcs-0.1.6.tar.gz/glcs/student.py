# -*- coding: utf-8 -*-
"""Student class."""


class StudentManager:
    """Supplies a set of operations for manipulating student objects."""

    def __init__(self, gl):
        pass


class Student:
    """Class to encapsulate student details.

    A convenience class that contains a gitlab.User object as well as
    student information gathered from a rosterfile.
    """

    def __init__(self, username, email, group_id, project_id, status):
        """Construct a student object."""
        self.username = username
        self.email = email
        self.group_id = group_id
        self.project_id = project_id
        self.status = status
