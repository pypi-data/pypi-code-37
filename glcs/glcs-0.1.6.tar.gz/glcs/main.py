# -*- coding: utf-8 -*-
"""Main class, GLCS. Contains a reference to all the manager classes."""
from glcs import course, project, student
import gitlab
from pathlib import Path


class GLCS:
    """Allows authenticated access to GitLab as well as GLCS utilities."""

    PG_CFG_PATH = Path.home() / ".python-gitlab.cfg"
    PG_CFG_SERVER = "gitlabt"

    def __init__(self, gl_server=None, gl_private=None):
        self.gitlab = None
        if gl_private is None and gl_server is not None:
            self.gitlab = gitlab.Gitlab.from_config(gl_server, [self.PG_CFG_PATH])
        elif gl_private is None and gl_server is None:
            self.gitlab = gitlab.Gitlab.from_config(self.PG_CFG_SERVER, [self.PG_CFG_PATH])
        else:
            self.gitlab = gitlab.Gitlab(gl_server, private_token=gl_private)
        self.courses = course.CourseManager(self.gitlab)
        self.projects = project.ProjectManager(self.gitlab)
        self.students = student.StudentManager(self.gitlab)
        """self.instructors = glcs.InstructorManager(self.gitlab)"""
