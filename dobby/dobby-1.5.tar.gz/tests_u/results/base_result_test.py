from unittest import TestCase
from unittest.mock import patch, Mock

from dobby.results.base_result import BaseResult


class BaseResultTestCase(TestCase):

    def test_initialization_sets_all_parameters(self):
        failed = "someFailed"
        status_code = "someCode"
        message = "someMessage"
        data = "somData"

        base_result = BaseResult(failed, status_code, message, data)

        self.assertEqual(base_result.failed, failed)
        self.assertEqual(base_result.status_code, status_code)
        self.assertEqual(base_result.message, message)
        self.assertEqual(base_result.data, data)
