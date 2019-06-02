"""Not found error"""

from ramses.errors.abstract import AbstractError
from ramses.status_codes import HTTPStatus


class NotFoundError(AbstractError):
    """HTTP Bad request error class"""

    statusCode = HTTPStatus.HTTP_400_BAD_REQUEST
    errorCode = '000000'

    def __init__(self, *details):
        """
        Constructor
        :param details: Additional description
        :type details: list
        """
        super().__init__('URL resource not found', *details)
