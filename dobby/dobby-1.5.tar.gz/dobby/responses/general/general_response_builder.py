import json

from dobby.responses.general.runtime_exception import RuntimeException
from dobby.results.base_result import BaseResult


class GeneralResponseBuilder:
    """A base class for all result builders"""

    def __init__(self):
        # TODO: do we need any kind of extra steps here?
        pass

    def create_response(self, result: BaseResult):
        result_as_json = json.dumps(result.__dict__)
        print(result_as_json)
        if result.failed:
            print('Received a failed result! Throwing an exception!')
            print(result.message)
            raise RuntimeException(result_as_json)
        return True

