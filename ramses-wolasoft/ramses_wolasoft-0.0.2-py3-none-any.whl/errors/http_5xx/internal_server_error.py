"""Internal ramses error"""

from ramses.errors.abstract import AbstractError


class InternalServerError(AbstractError):
    """Internal ramses error class"""

    statusCode = 500
    errorCode = '000000'

    def __init__(self, *details):
        """
        Constructor
        :param details: Additional description
        :type details: list
        """
        super().__init__('Internal ramses error', *details)
