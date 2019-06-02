"""Json response"""

from flask import Response, jsonify


# pylint: disable=too-many-ancestors
class JsonResponse(Response):
    """
    JsonResponse class

    Send back json like http response
    """

    @classmethod
    def force_type(cls, response, environ=None):
        """
        Force http response type
        :param response: Http response
        :param environ:
        :type response: flask.Response
        :return: Flask response
        :rtype: flask.Response
        """
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JsonResponse, cls,).force_type(response, environ)
