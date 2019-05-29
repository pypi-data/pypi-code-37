from unittest import TestCase
from unittest.mock import patch, Mock

from dobby.results.success_result import SuccessResult


class SuccessResultTestCase(TestCase):

    default_code = 200
    default_data = {}
    default_message = ""

    def test_initialization_with_nothing_uses_defaults(self):

        result = SuccessResult()

        self.assertFalse(result.failed)
        self.assertEqual(result.data, self.default_data)
        self.assertEqual(result.message, self.default_message)
        self.assertEqual(result.status_code, self.default_code)

    def test_initialization_with_message_sets_message(self):

        message = "someMessage"

        result = SuccessResult(message=message)

        self.assertFalse(result.failed)
        self.assertEqual(result.message, message)
        self.assertEqual(result.data, self.default_data)
        self.assertEqual(result.status_code, self.default_code)

    def test_initialization_with_data_sets_data(self):

        data = "someData"
        result = SuccessResult(data=data)

        self.assertFalse(result.failed)
        self.assertEqual(result.data, data)
        self.assertEqual(result.message, self.default_message)
        self.assertEqual(result.status_code, self.default_code)

    def test_initialization_with_code_sets_code(self):

        code = 200
        result = SuccessResult(status_code=code)

        self.assertFalse(result.failed)
        self.assertEqual(result.data, self.default_data)
        self.assertEqual(result.message, self.default_message)
        self.assertEqual(result.status_code, code)

    def test_initialization_with_all_custom_arguemnts_sets_all_custom_arguments(self):

        message = "someMessage"
        data = "someData"
        code = 200
        result = SuccessResult(status_code=code, data=data, message=message)

        self.assertFalse(result.failed)
        self.assertEqual(result.data, data)
        self.assertEqual(result.message, message)
        self.assertEqual(result.status_code, code)
