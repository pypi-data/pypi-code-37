"""Forbidden error"""

from ramses.errors.abstract import AbstractError
from ramses.status_codes import HTTPStatus


class ForbiddenError(AbstractError):
    """HTTP Forbidden error class"""

    statusCode = HTTPStatus.HTTP_403_FORBIDDEN
    errorCode = '000000'

    def __init__(self, *details):
        """
        Constructor
        :param details: Additional description
        :type details: list
        """
        super().__init__('Forbidden', *details)
