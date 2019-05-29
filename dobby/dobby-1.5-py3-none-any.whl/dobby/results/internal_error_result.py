from dobby.results.failed_result import FailedResult


class InternalErrorResult(FailedResult):

    def __init__(self, error_message: str, status_code: int = 500, data={}):
        super().__init__(error_message, status_code, data)
