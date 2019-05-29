from unittest import TestCase
from unittest.mock import patch, Mock

from dobby.events.sns.requests.message_list_sns_request import MessageListSNSRequest


class MessageListSNSRequestTestCase(TestCase):

    @patch('dobby.events.sns.requests.message_list_sns_request.BaseRequest.__init__')
    def test_uses_passed_messages_as_data_for_base_request(self, mock_base_request_class_constructor):

        some_messages = "someMessages"
        MessageListSNSRequest(some_messages)

        mock_base_request_class_constructor.assert_called_once_with(data=some_messages)
