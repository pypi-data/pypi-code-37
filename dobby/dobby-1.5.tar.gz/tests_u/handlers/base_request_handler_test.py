from unittest import TestCase
from unittest.mock import patch, Mock

from dobby.handlers.base_request_handler import BaseRequestHandler
from dobby.handlers.validation_error import ValidationError
from dobby.responses.general.general_response_builder import GeneralResponseBuilder
from dobby.results.internal_error_result import InternalErrorResult

MOCK_REQUEST_ADAPTER = Mock()
MOCK_RESPONSE_BUILDER = Mock(spec=GeneralResponseBuilder)


class BaseRequestHandlerTestCase(TestCase):

    def setUp(self):
        self.test_instance = BaseRequestHandler(
            MOCK_REQUEST_ADAPTER,
            MOCK_RESPONSE_BUILDER
        )

    @patch.object(BaseRequestHandler, '_try_handle')
    def test_handle__callsTryHandle(self, mock_try_handle):
        mock_try_handle.return_value = 'ok'

        self.test_instance.handle('someEvent', 'someContext')

        mock_try_handle.assert_called_once()

    @patch.object(BaseRequestHandler, '_try_handle')
    def test_handle_onSuccess_returnsResultFromTryHandle(self, mock_try_handle):
        expected_result = 'errorResult'
        mock_try_handle.return_value = expected_result

        result = self.test_instance.handle('someEvent', 'someContext')

        self.assertEqual(expected_result, result)

    @patch.object(MOCK_RESPONSE_BUILDER, 'create_response')
    @patch.object(BaseRequestHandler, '_try_handle')
    def test_handle_onErrorInTry_callsResultBuildingForInternalError(self, mock_try_handle, mock_create_response_method):
        mock_try_handle.side_effect = TypeError('Test')
        mock_create_response_method.return_value = 'ok'

        self.test_instance.handle('someEvent', 'someContext')

        mock_create_response_method.assert_called_once()
        parameter_of_call = mock_create_response_method.call_args_list[0][0][0]
        self.assertIsInstance(parameter_of_call, InternalErrorResult)

    @patch.object(MOCK_RESPONSE_BUILDER, 'create_response')
    @patch.object(BaseRequestHandler, '_try_handle')
    def test_handle_onErrorInTry_returnsTheBuiltError(self, mock_try_handle, mock_create_response_method):
        expected_result = 'errorResult'
        mock_try_handle.side_effect = Exception('Test')
        mock_create_response_method.return_value = expected_result

        result = self.test_instance.handle('someEvent', 'someContext')
        self.assertEqual(result, expected_result)

    @patch.object(MOCK_REQUEST_ADAPTER, 'translate')
    @patch.object(BaseRequestHandler, '_validate')
    @patch.object(BaseRequestHandler, '_execute')
    def test_try_handle_on_successful_run_calls_translate_validate_and_execute(self, mock_execute, mock_validate, mock_translate):
        translate_result = 'someReqeuest'
        mock_execute.return_value = 'ok'
        mock_validate.return_value = 'ok'
        mock_translate.return_value = translate_result

        self.test_instance._try_handle('someEvent', 'someContext')

        mock_translate.assert_called_once()
        mock_validate.assert_called_once_with(translate_result)
        mock_execute.assert_called_once_with(translate_result)

    @patch.object(MOCK_RESPONSE_BUILDER, 'create_response')
    @patch.object(MOCK_REQUEST_ADAPTER, 'translate')
    @patch.object(BaseRequestHandler, '_validate')
    @patch.object(BaseRequestHandler, '_execute')
    def test_try_handle_on_successful_run_returns_execution_result(self, mock_execute, mock_validate, mock_translate, mock_create_response):
        expected_result = 'okResult'
        mock_execute.return_value = expected_result
        mock_validate.return_value = 'ok'
        mock_translate.return_value = 'ok'
        mock_create_response.return_value = expected_result

        result = self.test_instance._try_handle('someEvent', 'someContext')

        self.assertEqual(result, expected_result)

    @patch('dobby.handlers.base_request_handler.FailedResult')
    @patch.object(MOCK_RESPONSE_BUILDER, 'create_response')
    @patch.object(MOCK_REQUEST_ADAPTER, 'translate')
    @patch.object(BaseRequestHandler, '_validate')
    def test_try_handle_on_validation_failure_builds_validation_failed_result(self, mock_validate, mock_translate, mock_create_response, failed_result_mock):
        error = ValidationError('test')
        mock_validate.side_effect = error
        mock_translate.return_value = 'ok'
        mock_create_response.return_value = 'ok'
        failed_result_instance = 'failedResultMock'
        failed_result_mock.return_value = failed_result_instance

        self.test_instance._try_handle('someEvent', 'someContext')

        mock_create_response.assert_called_once_with(failed_result_instance)

    @patch.object(MOCK_RESPONSE_BUILDER, 'create_response')
    @patch.object(MOCK_REQUEST_ADAPTER, 'translate')
    @patch.object(BaseRequestHandler, '_validate')
    def test_try_handle_on_validation_failure_returns_validation_failed_result(self, mock_validate, mock_translate, mock_create_response):
        expected_result = 'validationError'
        error = ValidationError('test')
        mock_validate.side_effect = error
        mock_translate.return_value = 'ok'
        mock_create_response.return_value = expected_result

        result = self.test_instance._try_handle('someEvent', 'someContext')

        self.assertEqual(result, expected_result)

    def test_validate_by_default_returns_true(self):
        result = self.test_instance._validate('someRequest')
        self.assertTrue(result)

    def test_report_validation_error_raises_ValidationError(self):
        try:
            self.test_instance._report_validation_error('someMessage')
            self.assertTrue(False)
        except ValidationError:
            self.assertTrue(True)
