from unittest import TestCase
from unittest.mock import patch

from dobby.events.sns.adapters.message_list_sns_adapter import MessageListSnsRequestAdapter


class MessageListSnsRequestAdapterTestCase(TestCase):

    def setUp(self):
        self.test_instance = MessageListSnsRequestAdapter()

    @patch('dobby.events.sns.adapters.message_list_sns_adapter.MessageListSNSRequest')
    def test_translate_translates_raw_input_into_expected_form(self, mock_request_class):
        raw_event = EVENT_DICTIONARY
        some_context = "someContext"

        expected_format = [
            "This is message 1",
            "This is message 2",
            "This is message 3"
        ]

        self.test_instance.translate(raw_event, some_context)

        mock_request_class.assert_called_once_with(expected_format)

    @patch('dobby.events.sns.adapters.message_list_sns_adapter.MessageListSNSRequest')
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
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:123456789012:lambda_topic:0b6941c3-f04d-4d3e-a66d-b1df00e1e381",
            "Sns": {
                "Type": "Notification",
                "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:lambda_topic",
                "Subject": "TestInvoke",
                "Message": "This is message 1",
                "Timestamp": "2015-04-02T07:36:57.451Z",
                "SignatureVersion": "1",
                "Signature": "r0Dc5YVHuAglGcmZ9Q7SpFb2PuRDFmJNprJlAEEk8CzSq9Btu8U7dxOu++uU",
                "SigningCertUrl": "http://sns.us-east-1.amazonaws.com/SimpleNotificationService-d6d679a1d18e95c2f9ffcf11f4f9e198.pem",
                "UnsubscribeUrl": "http://cloudcast.amazon.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:123456789012:example_topic:0b6941c3-f04d-4d3e-a66d-b1df00e1e381",
                "MessageAttributes": {"key": {"Type": "String", "Value": "value"}}
            }
        },
{
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:123456789012:lambda_topic:0b6941c3-f04d-4d3e-a66d-b1df00e1e381",
            "Sns": {
                "Type": "Notification",
                "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:lambda_topic",
                "Subject": "TestInvoke",
                "Message": "This is message 2",
                "Timestamp": "2015-04-02T07:36:57.451Z",
                "SignatureVersion": "1",
                "Signature": "r0Dc5YVHuAglGcmZ9Q7SpFb2PuRDFmJNprJlAEEk8CzSq9Btu8U7dxOu++uU",
                "SigningCertUrl": "http://sns.us-east-1.amazonaws.com/SimpleNotificationService-d6d679a1d18e95c2f9ffcf11f4f9e198.pem",
                "UnsubscribeUrl": "http://cloudcast.amazon.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:123456789012:example_topic:0b6941c3-f04d-4d3e-a66d-b1df00e1e381",
                "MessageAttributes": {"key": {"Type": "String", "Value": "value"}}
            }
        },
{
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:123456789012:lambda_topic:0b6941c3-f04d-4d3e-a66d-b1df00e1e381",
            "Sns": {
                "Type": "Notification",
                "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:lambda_topic",
                "Subject": "TestInvoke",
                "Message": "This is message 3",
                "Timestamp": "2015-04-02T07:36:57.451Z",
                "SignatureVersion": "1",
                "Signature": "r0Dc5YVHuAglGcmZ9Q7SpFb2PuRDFmJNprJlAEEk8CzSq9Btu8U7dxOu++uU",
                "SigningCertUrl": "http://sns.us-east-1.amazonaws.com/SimpleNotificationService-d6d679a1d18e95c2f9ffcf11f4f9e198.pem",
                "UnsubscribeUrl": "http://cloudcast.amazon.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:123456789012:example_topic:0b6941c3-f04d-4d3e-a66d-b1df00e1e381",
                "MessageAttributes": {"key": {"Type": "String", "Value": "value"}}
            }
        }
    ]
}
