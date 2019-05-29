from unittest import TestCase

from dobby.responses.general.runtime_exception import RuntimeException


class RuntimeExceptionTestCase(TestCase):

    def test_init_sets_date(self):
        given_data = "given data"

        test_instance = RuntimeException(given_data)

        self.assertEqual(given_data, test_instance.args[0])
