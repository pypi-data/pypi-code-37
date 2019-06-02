"""Abstract error"""

from abc import ABCMeta
import stringcase


# pylint: disable-msg=R0801
class AbstractError(Exception):
    """Abstract error class"""
    __metaclass__ = ABCMeta

    errorCode = '000000'
    statusCode = 500

    # pylint: disable-msg=R0801
    def __init__(self, message, *details):
        """
        Constructor
        :param message: Message error
        :param details: Error details or technical data
        :type message: str
        :type message: list
        """
        self.message = message
        self.details = self.technical_data(*details)
        Exception.__init__(self)

    # pylint: disable-msg=R0801
    @staticmethod
    def technical_data(*details):
        """
        Format error details
        :param details: Error details
        :type details: list
        :return: Dictionary containing formatted error
        :rtype: dict
        """
        if details:
            data = dict()
            for detail in details:
                data.update({stringcase.camelcase(detail.lower()): True})
            return data

        return None

    # pylint: disable-msg=R0801
    def to_json(self):
        """Transform output error json format"""
        error = dict(
            errorCode=self.errorCode,
            details=self.details,
            message=self.message,
            statusCode=self.statusCode
        )

        return error
