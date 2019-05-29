import json

from dobby.responses.general.general_response_builder import GeneralResponseBuilder
from dobby.responses.http.response.http_response import HttpResponse
from dobby.results.base_result import BaseResult


class HTTPResponseBuilder(GeneralResponseBuilder):

    def __init__(self):
        super().__init__()

    def create_response(self, result: BaseResult):

        status_code = result.status_code
        print(status_code)
        response_body = self._prepare_jsonified_response_body(result)
        return HttpResponse(status_code, response_body).format()

    def _prepare_jsonified_response_body(self, result: BaseResult):
        response_body = self._prepare_response_body(result)
        return json.dumps(response_body, default=self._get_dict_lambda())

    def _prepare_response_body(self, result: BaseResult):
        failed = result.failed
        message = result.message
        data = result.data

        response_body = dict()
        response_body.update({"__failed": failed})
        if data:
            response_body.update({"data": data})
        if message:
            response_body.update({"message": message})

        print(response_body)
        return response_body

    def _get_dict_lambda(self):
        return lambda x: x.__dict__
