from unittest import TestCase
from unittest.mock import patch, Mock

from dobby.responses.http.builder.http_response_builder import HTTPResponseBuilder
from dobby.responses.general.general_response_builder import GeneralResponseBuilder

MOCK_RESULT = Mock()


class BaseRequestHandlerTestCase(TestCase):

    def setUp(self):
        self.test_instance = HTTPResponseBuilder()
        MOCK_RESULT.reset_mock()

    def test_complies_to_base_response_builder(self):
        base_keys = dir(GeneralResponseBuilder())
        http_keys = dir(HTTPResponseBuilder())

        for attribute in base_keys:
            self.assertIn(attribute, http_keys)

    @patch("dobby.responses.http.builder.http_response_builder.HttpResponse")
    @patch.object(HTTPResponseBuilder, '_prepare_jsonified_response_body')
    def test_create_response_uses_result_status_code(self, mock_response_preparation, mock_http_response):
        expected_status_code = "someStatusCode"
        expected_body = "someBody"
        MOCK_RESULT = Mock(status_code=expected_status_code)

        mock_response_preparation.return_value = expected_body

        self.test_instance.create_response(MOCK_RESULT)

        mock_response_preparation.assert_called_once_with(MOCK_RESULT)
        mock_http_response.assert_called_once_with(
            expected_status_code,
            expected_body
        )
        mock_http_response.return_value.format.assert_called_once()

    @patch('json.dumps')
    @patch.object(HTTPResponseBuilder, '_get_dict_lambda')
    @patch.object(HTTPResponseBuilder, '_prepare_response_body')
    def test__prepare_jsonified_response_body_prepares_response_body_using_result(self,
                                                                                  mock_prepare_response_body_method,
                                                                                  mock_get_dict_lambda_method,
                                                                                  mock_json_dumps_method):
        expected_body = "someBody"
        expected_function = "some function"

        mock_prepare_response_body_method.return_value = expected_body
        mock_get_dict_lambda_method.return_value = expected_function

        result = "someResult"
        self.test_instance._prepare_jsonified_response_body(result)

        mock_prepare_response_body_method.assert_called_once_with(result)

        mock_json_dumps_method.assert_called_once_with(expected_body, default=expected_function)

    @patch('json.dumps')
    @patch.object(HTTPResponseBuilder, '_prepare_response_body')
    def test__prepare_jsonified_response_body_returns_result_of_json_dump(self, mock_prepare_response_body_method,
                                                                          mock_json_dumps_method):
        expected_json_dump = "someJsonDump"

        mock_json_dumps_method.return_value = expected_json_dump

        result = "someResult"
        body = self.test_instance._prepare_jsonified_response_body(result)

        self.assertEqual(body, expected_json_dump)

    def test__prepare_response_body_returns_dict_with_failed_of_supplied_result(self):
        expected_failed = "someFailed"

        mock_result = Mock(failed=expected_failed, message="", data={})

        expected_body = {
            "__failed": expected_failed
        }
        response_body = self.test_instance._prepare_response_body(mock_result)

        self.assertEqual(response_body, expected_body)

    def test__prepare_response_body_returns_dict_with_only_message_and_failed(self):
        expected_failed = "someFailed"
        expected_message = "someMessage"

        mock_result = Mock(
            failed=expected_failed,
            message=expected_message,
            data={}
        )

        expected_body = {
            "__failed": expected_failed,
            "message": expected_message
        }
        response_body = self.test_instance._prepare_response_body(mock_result)

        self.assertEqual(response_body, expected_body)

    def test__prepare_response_body_returns_dict_with_only_data_and_failed(self):
        expected_failed = "someFailed"
        expected_data = "someData"

        mock_result = Mock(
            failed=expected_failed,
            message="",
            data=expected_data
        )

        expected_body = {
            "__failed": expected_failed,
            "data": expected_data
        }
        response_body = self.test_instance._prepare_response_body(mock_result)

        self.assertEqual(response_body, expected_body)

    def test__prepare_response_body_returns_dict_with_all_specified_result_attributes(self):
        expected_failed = "someFailed"
        expected_message = "someMessage"
        expected_data = "someData"

        mock_result = Mock(
            failed=expected_failed,
            message=expected_message,
            data=expected_data
        )

        expected_body = {
            "__failed": expected_failed,
            "message": expected_message,
            "data": expected_data
        }
        response_body = self.test_instance._prepare_response_body(mock_result)

        self.assertEqual(response_body, expected_body)

    def test__get_dict_lambda_returns_function_that_gets_dict(self):
        expected_value = {"value": "the expected value"}
        given_value = DictTestClass(expected_value)

        received_lambda = self.test_instance._get_dict_lambda()
        x = given_value.__dict__
        received_value = received_lambda(given_value)

        self.assertEqual(received_value, expected_value)


class DictTestClass:
    def __init__(self, dict_value):
        self.__dict__ = dict_value
