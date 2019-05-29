# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class VerifyPhoneResponse(object):
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
        'phone': 'str',
        'api_key': 'str',
        'msg': 'str'
    }

    attribute_map = {
        'status': 'status',
        'phone': 'phone',
        'api_key': 'api_key',
        'msg': 'msg'
    }

    def __init__(self, status=None, phone=None, api_key=None, msg=None):  # noqa: E501
        """VerifyPhoneResponse - a model defined in spec"""  # noqa: E501
        self._status = None
        self._phone = None
        self._api_key = None
        self._msg = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if phone is not None:
            self.phone = phone
        if api_key is not None:
            self.api_key = api_key
        if msg is not None:
            self.msg = msg

    @property
    def status(self):
        """Gets the status of this VerifyPhoneResponse.  # noqa: E501


        :return: The status of this VerifyPhoneResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this VerifyPhoneResponse.


        :param status: The status of this VerifyPhoneResponse.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def phone(self):
        """Gets the phone of this VerifyPhoneResponse.  # noqa: E501


        :return: The phone of this VerifyPhoneResponse.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this VerifyPhoneResponse.


        :param phone: The phone of this VerifyPhoneResponse.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def api_key(self):
        """Gets the api_key of this VerifyPhoneResponse.  # noqa: E501


        :return: The api_key of this VerifyPhoneResponse.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this VerifyPhoneResponse.


        :param api_key: The api_key of this VerifyPhoneResponse.  # noqa: E501
        :type: str
        """

        self._api_key = api_key

    @property
    def msg(self):
        """Gets the msg of this VerifyPhoneResponse.  # noqa: E501


        :return: The msg of this VerifyPhoneResponse.  # noqa: E501
        :rtype: str
        """
        return self._msg

    @msg.setter
    def msg(self, msg):
        """Sets the msg of this VerifyPhoneResponse.


        :param msg: The msg of this VerifyPhoneResponse.  # noqa: E501
        :type: str
        """

        self._msg = msg

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
        if issubclass(VerifyPhoneResponse, dict):
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
        if not isinstance(other, VerifyPhoneResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
