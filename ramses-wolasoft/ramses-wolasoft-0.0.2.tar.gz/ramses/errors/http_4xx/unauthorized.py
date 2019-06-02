"""Unauthorized error"""

from ramses.errors.abstract import AbstractError
from ramses.status_codes import HTTPStatus


class UnauthorizedError(AbstractError):
    """HTTP Unauthorized error class"""

    statusCode = HTTPStatus.HTTP_401_UNAUTHORIZED
    errorCode = '000000'

    def __init__(self, *details):
        """
        Constructor
        :param details: Additional description
        :type details: list
        """
        super().__init__('Unauthorized', *details)
