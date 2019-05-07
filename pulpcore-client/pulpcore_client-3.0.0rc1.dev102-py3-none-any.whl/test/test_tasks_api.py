# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    OpenAPI spec version: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.api.tasks_api import TasksApi  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException


class TestTasksApi(unittest.TestCase):
    """TasksApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulpcore.api.tasks_api.TasksApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_tasks_cancel(self):
        """Test case for tasks_cancel

        Cancel a task  # noqa: E501
        """
        pass

    def test_tasks_delete(self):
        """Test case for tasks_delete

        Delete a task  # noqa: E501
        """
        pass

    def test_tasks_list(self):
        """Test case for tasks_list

        List tasks  # noqa: E501
        """
        pass

    def test_tasks_read(self):
        """Test case for tasks_read

        Inspect a task  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
