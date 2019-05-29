from unittest import TestCase
from dobby.events.base.requests.base_request import BaseRequest


class BaseRequestTestCase(TestCase):

    def setUp(self):
        pass

    def test_getData__DefaultsToEmptyObject(self):
        test_instance = BaseRequest()
        self.assertEqual(test_instance.data, {})

    def test_getData__SpecifiedValue(self):
        provided_value = {"SomeProperty": "SomeValue"}
        test_instance = BaseRequest(provided_value)

        self.assertEqual(test_instance.data, provided_value)
