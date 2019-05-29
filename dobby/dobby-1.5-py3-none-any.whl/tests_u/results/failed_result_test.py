from unittest import TestCase
from unittest.mock import patch, Mock

from dobby.results.failed_result import FailedResult


class FailedResultTestCase(TestCase):

    def test_initialization_with_message_sets_only_message(self):
        expected_code = 400
        expected_data = {}

        message = "someMessage"

        result = FailedResult(message)

        self.assertTrue(result.failed)
        self.assertEqual(result.message, message)
        self.assertEqual(result.data, expected_data)
        self.assertEqual(result.status_code, expected_code)

    def test_initialization_with_message_and_data_sets_data(self):
        expected_code = 400

        data = "someData"
        message = "someMessage"

        result = FailedResult(message, data=data)

        self.assertTrue(result.failed)
        self.assertEqual(result.data, data)
        self.assertEqual(result.message, message)
        self.assertEqual(result.status_code, expected_code)

    def test_initialization_with_message_and_data_and_code_sets_data(self):
        code = 406
        data = "someData"
        message = "someMessage"

        result = FailedResult(message, data=data, status_code=code)

        self.assertTrue(result.failed)
        self.assertEqual(result.data, data)
        self.assertEqual(result.message, message)
        self.assertEqual(result.status_code, code)
