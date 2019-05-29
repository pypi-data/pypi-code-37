from unittest import TestCase
from unittest.mock import patch

from dobby.events.base.adapters.base_request_adapter import BaseRequestAdapter


class BaseRequestAdapterTestCase(TestCase):

    def setUp(self):
        self.test_instance = BaseRequestAdapter()

    @patch('dobby.events.base.adapters.base_request_adapter.BaseRequest')
    def test_translates_returns_an_instance_if_empty_base_request(self, mock_base_request_class):
        event = 'someEvent'
        context = 'someContenxt'

        expected_request = 'some_request'
        mock_base_request_class.return_value = expected_request

        result = self.test_instance.translate(event, context)

        mock_base_request_class.assert_called_once_with()
        self.assertEqual(result, expected_request)
