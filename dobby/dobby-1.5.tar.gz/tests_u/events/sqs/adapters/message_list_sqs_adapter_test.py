from unittest import TestCase
from unittest.mock import patch, Mock

from dobby.events.sqs.adapters.message_list_sqs_adapter import MessageListSqsRequestAdapter


class MessageListSqsRequestAdapterTestCase(TestCase):

    def setUp(self):
        self.test_instance = MessageListSqsRequestAdapter()

    @patch('dobby.events.sqs.adapters.message_list_sqs_adapter.MessageListSQSRequest')
    def test_translate_translates_raw_input_into_expected_form(self, mock_request_class):
        
        raw_event = EVENT_DICTIONARY
        some_context = "someContext"

        expected_format = [
            {"attribute":"value"}, 
            {"key":"value"}, 
            {"field":"value"}, 
        ]

        self.test_instance.translate(raw_event, some_context)

        mock_request_class.assert_called_once_with(expected_format)


    @patch('dobby.events.sqs.adapters.message_list_sqs_adapter.MessageListSQSRequest')
    def test_translate_returns_the_resulting_request_object(self, mock_request_class):
        
        raw_event = EVENT_DICTIONARY
        some_context = "someContext"

        expected_request_object = "someObject"
        mock_request_class.return_value = expected_request_object

        result = self.test_instance.translate(raw_event, some_context)

        self.assertEqual(result, expected_request_object)



EVENT_DICTIONARY = {
    "Records": [
        {
            "messageId": "some_id_1",
            "receiptHandle": "some_recepit",
            "body": "{\"attribute\": \"value\"}",
            "attributes": {
                "ApproximateReceiveCount": "3",
                "SentTimestamp": "1547124936186",
                "SenderId": "abc",
                "ApproximateFirstReceiveTimestamp": "1547125534910"
            },
            "messageAttributes": {},
            "md5OfBody": "asdasd",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:xxxxxxx:xxxxxxx:yyyyy",
            "awsRegion": "xxxxxxx"
        },
        {
            "messageId": "some_id_2",
            "receiptHandle": "some_recepit",
            "body": "{\"key\": \"value\"}",
            "attributes": {
                "ApproximateReceiveCount": "3",
                "SentTimestamp": "1547124936186",
                "SenderId": "abc",
                "ApproximateFirstReceiveTimestamp": "1547125534910"
            },
            "messageAttributes": {},
            "md5OfBody": "asdasd",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:xxxxxxx:xxxxxxx:yyyyy",
            "awsRegion": "xxxxxxx"
        },
         {
            "messageId": "some_id_3",
            "receiptHandle": "some_recepit",
            "body": "{\"field\": \"value\"}",
            "attributes": {
                "ApproximateReceiveCount": "3",
                "SentTimestamp": "1547124936186",
                "SenderId": "abc",
                "ApproximateFirstReceiveTimestamp": "1547125534910"
            },
            "messageAttributes": {},
            "md5OfBody": "asdasd",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:xxxxxxx:xxxxxxx:yyyyy",
            "awsRegion": "xxxxxxx"
        },
    ]
}
