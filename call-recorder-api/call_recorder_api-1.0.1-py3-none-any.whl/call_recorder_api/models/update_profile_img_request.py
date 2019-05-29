# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class UpdateProfileImgRequest(object):
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
        'api_key': 'str',
        'file': 'str'
    }

    attribute_map = {
        'api_key': 'api_key',
        'file': 'file'
    }

    def __init__(self, api_key=None, file=None):  # noqa: E501
        """UpdateProfileImgRequest - a model defined in spec"""  # noqa: E501
        self._api_key = None
        self._file = None
        self.discriminator = None
        self.api_key = api_key
        if file is not None:
            self.file = file

    @property
    def api_key(self):
        """Gets the api_key of this UpdateProfileImgRequest.  # noqa: E501


        :return: The api_key of this UpdateProfileImgRequest.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this UpdateProfileImgRequest.


        :param api_key: The api_key of this UpdateProfileImgRequest.  # noqa: E501
        :type: str
        """
        if api_key is None:
            raise ValueError("Invalid value for `api_key`, must not be `None`")  # noqa: E501

        self._api_key = api_key

    @property
    def file(self):
        """Gets the file of this UpdateProfileImgRequest.  # noqa: E501


        :return: The file of this UpdateProfileImgRequest.  # noqa: E501
        :rtype: str
        """
        return self._file

    @file.setter
    def file(self, file):
        """Sets the file of this UpdateProfileImgRequest.


        :param file: The file of this UpdateProfileImgRequest.  # noqa: E501
        :type: str
        """

        self._file = file

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
        if issubclass(UpdateProfileImgRequest, dict):
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
        if not isinstance(other, UpdateProfileImgRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
