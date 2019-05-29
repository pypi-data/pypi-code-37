# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class RegisterPhoneRequest(object):
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
        'token': 'str',
        'phone': 'str'
    }

    attribute_map = {
        'token': 'token',
        'phone': 'phone'
    }

    def __init__(self, token=None, phone=None):  # noqa: E501
        """RegisterPhoneRequest - a model defined in spec"""  # noqa: E501
        self._token = None
        self._phone = None
        self.discriminator = None
        self.token = token
        self.phone = phone

    @property
    def token(self):
        """Gets the token of this RegisterPhoneRequest.  # noqa: E501


        :return: The token of this RegisterPhoneRequest.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this RegisterPhoneRequest.


        :param token: The token of this RegisterPhoneRequest.  # noqa: E501
        :type: str
        """
        if token is None:
            raise ValueError("Invalid value for `token`, must not be `None`")  # noqa: E501

        self._token = token

    @property
    def phone(self):
        """Gets the phone of this RegisterPhoneRequest.  # noqa: E501


        :return: The phone of this RegisterPhoneRequest.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this RegisterPhoneRequest.


        :param phone: The phone of this RegisterPhoneRequest.  # noqa: E501
        :type: str
        """
        if phone is None:
            raise ValueError("Invalid value for `phone`, must not be `None`")  # noqa: E501

        self._phone = phone

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
        if issubclass(RegisterPhoneRequest, dict):
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
        if not isinstance(other, RegisterPhoneRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
