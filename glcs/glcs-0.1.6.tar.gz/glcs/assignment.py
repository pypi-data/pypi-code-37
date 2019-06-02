# -*- coding: utf-8 -*-
"""AssignmentManager and LabManager classes."""
# TODO:
#   [ ] - Sign in as gitlabadm and look for system hook setting
#   [ ] - Create a test 'hook server' and see if it works
#   [ ] -
import json
from pathlib import Path


class AssignmentManager:
    """Handles common Assignment manipulation tasks."""

    def __init__(self, course_name, gitlab=None):
        """Set up Gitlab and gathers instructor information."""
        self.gitlab = gitlab
        self.course_name = course_name

    def create(self, *, type, tag, due, mimir_id=None):
        """Create an assignment for this course."""
        course = self.course_name
        output_dict = {}
        output_dict['course_name'] = course
        output_dict['tag_name'] = tag
        output_dict['due_date'] = due.isoformat()
        if mimir_id is not None:
            output_dict['mimir_id'] = mimir_id

        # Does nothing right now to actually create the assignment


class Assignment:
    """Represents an assignment."""

    def __init__(self, course_name, type, tag=None, due=None, mimir_id=None):
        self.course = course_name
        self.type = type
        self.tag = tag
        self.due = due
        self.mimir_id = mimir_id

    def course(self, c=None):
        if c is None:
            return self.course
        self.course = c

    def type(self, t=None):
        if t is None:
            return self.type
        self.type = t

    def tag(self, t=None):
        if t is None:
            return self.tag
        self.tag = t

    def due(self, d=None):
        if d is None:
            return self.due
        self.due = d

    def mimir_id(self, m=None):
        if m is None:
            return self.mimir_id
        self.mimir_id = m
