from unittest import TestCase
from unittest.mock import patch, Mock

from dobby.events.sqs.requests.message_list_sqs_request import MessageListSQSRequest


class MessageListSQSRequestTestCase(TestCase):

    @patch('dobby.events.sqs.requests.message_list_sqs_request.BaseRequest.__init__')
    def test_uses_passed_messages_as_data_for_base_request(self, mock_base_request_class_constructor):

        some_messages = "someMessages"
        MessageListSQSRequest(some_messages)

        mock_base_request_class_constructor.assert_called_once_with(data=some_messages)
