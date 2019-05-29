from unittest import TestCase
from dobby.events.http.requests.http_request import HTTPRequest


class HTTPRequestTestCase(TestCase):

    def setUp(self):
        pass

    def test_getPathParameters__SetValue(self):
        provided_value = {"id": "5"}
        event = dict()
        event['body'] = """ {} """
        event['pathParameters'] = provided_value
        event['queryStringParameters'] = ''
        test_instance = HTTPRequest(event, "someContext")

        self.assertEqual(test_instance.getPathParameters(), provided_value)

    def test_getQueryStringParameters__SetValue(self):
        provided_value = {"id": "5"}
        event = dict()
        event['body'] = """ {} """
        event['pathParameters'] = ''
        event['queryStringParameters'] = provided_value
        test_instance = HTTPRequest(event, "someContext")

        self.assertEqual(test_instance.getQueryStringParameters(), provided_value)

    def test_getRequestContext__SetValue(self):
        provided_value = {"id": "5"}
        event = dict()
        event['body'] = """ {} """
        event['pathParameters'] = ''
        event['queryStringParameters'] = ''
        test_instance = HTTPRequest(event, provided_value)

        self.assertEqual(test_instance.getRequestContext(), provided_value)


