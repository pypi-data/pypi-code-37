from unittest import TestCase

from dobby.responses.general.general_response import GeneralResponse


class GeneralResponseTestCase(TestCase):

    def test_init_sets_date(self):
        given_data = "given data"

        test_instance = GeneralResponse(given_data)

        self.assertEqual(given_data, test_instance.data)
