"""Server error mapper"""

import ast
from flask import jsonify
from ramses.errors.http_4xx.bad_request_error import BadRequestError
from ramses.errors.http_4xx.forbidden import ForbiddenError
from ramses.errors.http_4xx.not_found_error import NotFoundError
from ramses.errors.http_4xx.unauthorized import UnauthorizedError


def http400(error):
    """
    Http 400 error mapper
    :param error: Exception
    :return: None
    """
    response = jsonify(ast.literal_eval(error.messages))
    response.status_code = BadRequestError.statusCode
    return response


# pylint: disable=unused-argument
def http404(error):
    """
    Http 404 error mapper
    :param error: Exception
    :return: None
    """
    response = jsonify(NotFoundError().to_json())
    response.status_code = NotFoundError.statusCode
    return response


# pylint: disable=unused-argument
def http401(error):
    """
    Http 401 error mapper
    :param error: Exception
    :return: None
    """
    response = jsonify(UnauthorizedError().to_json())
    response.status_code = UnauthorizedError.statusCode
    return response


# pylint: disable=unused-argument
def http403(error):
    """
    Http 403 error mapper
    :param error: Exception
    :return: None
    """
    response = jsonify(ForbiddenError().to_json())
    response.status_code = ForbiddenError.statusCode
    return response
