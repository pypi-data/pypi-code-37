# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six
from call_recorder_api.models.get_languages_response_languages import GetLanguagesResponseLanguages  # noqa: F401,E501


class GetLanguagesResponse(object):
    """NOTE: 

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'status': 'str',
        'msg': 'str',
        'languages': 'list[GetLanguagesResponseLanguages]'
    }

    attribute_map = {
        'status': 'status',
        'msg': 'msg',
        'languages': 'languages'
    }

    def __init__(self, status=None, msg=None, languages=None):  # noqa: E501
        """GetLanguagesResponse - a model defined in spec"""  # noqa: E501
        self._status = None
        self._msg = None
        self._languages = None
        self.discriminator = None
        self.status = status
        if msg is not None:
            self.msg = msg
        if languages is not None:
            self.languages = languages

    @property
    def status(self):
        """Gets the status of this GetLanguagesResponse.  # noqa: E501


        :return: The status of this GetLanguagesResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this GetLanguagesResponse.


        :param status: The status of this GetLanguagesResponse.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def msg(self):
        """Gets the msg of this GetLanguagesResponse.  # noqa: E501


        :return: The msg of this GetLanguagesResponse.  # noqa: E501
        :rtype: str
        """
        return self._msg

    @msg.setter
    def msg(self, msg):
        """Sets the msg of this GetLanguagesResponse.


        :param msg: The msg of this GetLanguagesResponse.  # noqa: E501
        :type: str
        """

        self._msg = msg

    @property
    def languages(self):
        """Gets the languages of this GetLanguagesResponse.  # noqa: E501


        :return: The languages of this GetLanguagesResponse.  # noqa: E501
        :rtype: list[GetLanguagesResponseLanguages]
        """
        return self._languages

    @languages.setter
    def languages(self, languages):
        """Sets the languages of this GetLanguagesResponse.


        :param languages: The languages of this GetLanguagesResponse.  # noqa: E501
        :type: list[GetLanguagesResponseLanguages]
        """

        self._languages = languages

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(GetLanguagesResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GetLanguagesResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
