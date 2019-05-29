from unittest import TestCase

from dobby.responses.general.general_response_builder import GeneralResponseBuilder
from dobby.responses.general.runtime_exception import RuntimeException
from dobby.results.failed_result import FailedResult
from dobby.results.success_result import SuccessResult


class GeneralResponseBuilderTestCase(TestCase):

    def setUp(self):
        self.test_instance = GeneralResponseBuilder()

    def test_create_response_when_result_successful_then_returns_true(self):
        given_result = SuccessResult()

        received_value = self.test_instance.create_response(given_result)

        self.assertEqual(True, received_value)

    def test_create_response_when_result_unsuccessful_then_raises_RunTimeException(self):
        given_result = FailedResult("this was an error")

        try:
            self.test_instance.create_response(given_result)
            self.fail("Should've thrown an error")
        except RuntimeException:
            pass
        except:
            self.fail("Should've thrown a RuntimeException")
