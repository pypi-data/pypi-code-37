# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class UpdateProfileRequestData(object):
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
        'f_name': 'str',
        'l_name': 'str',
        'email': 'str',
        'is_public': 'bool',
        'language': 'str'
    }

    attribute_map = {
        'f_name': 'f_name',
        'l_name': 'l_name',
        'email': 'email',
        'is_public': 'is_public',
        'language': 'language'
    }

    def __init__(self, f_name=None, l_name=None, email=None, is_public=None, language=None):  # noqa: E501
        """UpdateProfileRequestData - a model defined in spec"""  # noqa: E501
        self._f_name = None
        self._l_name = None
        self._email = None
        self._is_public = None
        self._language = None
        self.discriminator = None
        if f_name is not None:
            self.f_name = f_name
        if l_name is not None:
            self.l_name = l_name
        if email is not None:
            self.email = email
        if is_public is not None:
            self.is_public = is_public
        if language is not None:
            self.language = language

    @property
    def f_name(self):
        """Gets the f_name of this UpdateProfileRequestData.  # noqa: E501


        :return: The f_name of this UpdateProfileRequestData.  # noqa: E501
        :rtype: str
        """
        return self._f_name

    @f_name.setter
    def f_name(self, f_name):
        """Sets the f_name of this UpdateProfileRequestData.


        :param f_name: The f_name of this UpdateProfileRequestData.  # noqa: E501
        :type: str
        """

        self._f_name = f_name

    @property
    def l_name(self):
        """Gets the l_name of this UpdateProfileRequestData.  # noqa: E501


        :return: The l_name of this UpdateProfileRequestData.  # noqa: E501
        :rtype: str
        """
        return self._l_name

    @l_name.setter
    def l_name(self, l_name):
        """Sets the l_name of this UpdateProfileRequestData.


        :param l_name: The l_name of this UpdateProfileRequestData.  # noqa: E501
        :type: str
        """

        self._l_name = l_name

    @property
    def email(self):
        """Gets the email of this UpdateProfileRequestData.  # noqa: E501


        :return: The email of this UpdateProfileRequestData.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UpdateProfileRequestData.


        :param email: The email of this UpdateProfileRequestData.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def is_public(self):
        """Gets the is_public of this UpdateProfileRequestData.  # noqa: E501


        :return: The is_public of this UpdateProfileRequestData.  # noqa: E501
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this UpdateProfileRequestData.


        :param is_public: The is_public of this UpdateProfileRequestData.  # noqa: E501
        :type: bool
        """

        self._is_public = is_public

    @property
    def language(self):
        """Gets the language of this UpdateProfileRequestData.  # noqa: E501


        :return: The language of this UpdateProfileRequestData.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this UpdateProfileRequestData.


        :param language: The language of this UpdateProfileRequestData.  # noqa: E501
        :type: str
        """

        self._language = language

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
        if issubclass(UpdateProfileRequestData, dict):
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
        if not isinstance(other, UpdateProfileRequestData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
