"""Server error mapper"""

from flask import jsonify
from .internal_server_error import InternalServerError


# pylint: disable=unused-argument
def http500(error):
    """
    Http http_5xx error mapper
    :param error: Exception
    :return: None
    """
    response = jsonify(InternalServerError().to_json())
    response.status_code = InternalServerError.statusCode
    return response
