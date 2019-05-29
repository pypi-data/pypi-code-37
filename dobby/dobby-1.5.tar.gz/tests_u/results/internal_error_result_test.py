from unittest import TestCase
from unittest.mock import patch, Mock

from dobby.results.internal_error_result import InternalErrorResult


class InternalErrorResultTestCase(TestCase):

    default_code = 500
    default_data = {}

    def test_initialization_with_message_sets_only_message(self):

        message = "someMessage"

        result = InternalErrorResult(message)

        self.assertTrue(result.failed)
        self.assertEqual(result.message, message)
        self.assertEqual(result.data, self.default_data)
        self.assertEqual(result.status_code, self.default_code)

    def test_initialization_with_message_and_data_sets_data(self):

        data = "someData"
        message = "someMessage"

        result = InternalErrorResult(message, data=data)

        self.assertTrue(result.failed)
        self.assertEqual(result.data, data)
        self.assertEqual(result.message, message)
        self.assertEqual(result.status_code, self.default_code)

    def test_initialization_with_message_and_data_and_code_sets_data(self):
        code = 55555
        data = "someData"
        message = "someMessage"

        result = InternalErrorResult(message, data=data, status_code=code)

        self.assertTrue(result.failed)
        self.assertEqual(result.data, data)
        self.assertEqual(result.message, message)
        self.assertEqual(result.status_code, code)
