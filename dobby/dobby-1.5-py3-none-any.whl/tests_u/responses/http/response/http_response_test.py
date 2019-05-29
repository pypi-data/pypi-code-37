from unittest import TestCase
from unittest.mock import Mock, patch

from dobby.responses.http.response.http_response import HttpResponse


class HttpResponseTestCase(TestCase):

    def test_construction_from_status_code_and_body_adds_headers(self):
        expected_status_code = "someStatusCode"
        expected_body = "someBody"

        test_instance = HttpResponse(expected_status_code, expected_body)

        self.assertEqual(test_instance.statusCode, expected_status_code)
        self.assertEqual(test_instance.body, expected_body)
        self.assertIsNotNone(test_instance.headers)

    def test_format_to_aws_returns_dict_with_attributes_in_right_convention(self):

        expected_status_code = "someStatusCode"
        expected_body = "someBody"
        expected_headers = "someHeaders"

        expected_dict = {
            "statusCode": expected_status_code,
            "body": expected_body,
            "headers": expected_headers
        }

        test_instance = HttpResponse(expected_status_code, expected_body)
        test_instance.headers = expected_headers
        format_result = test_instance.format()

        self.assertEqual(format_result, expected_dict)
