from unittest import TestCase
from dobby.handlers.validation_error import ValidationError


class ValidationErrorTestCase(TestCase):

    def setUp(self):
        pass

    def test_constructor__MessagePassedToSuper(self):
        provided_value = "SomeValue"
        test_instance = ValidationError(provided_value)

        self.assertEqual(test_instance.message, provided_value)

    def test_constructor__DefaultsToNonEmptyString(self):
        test_instance = ValidationError()

        self.assertTrue(test_instance)
