# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class GetPhonesResponseInner(object):
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
        'phone_number': 'str',
        'number': 'str',
        'prefix': 'str',
        'friendly_name': 'str',
        'flag': 'str',
        'city': 'str',
        'country': 'str'
    }

    attribute_map = {
        'phone_number': 'phone_number',
        'number': 'number',
        'prefix': 'prefix',
        'friendly_name': 'friendly_name',
        'flag': 'flag',
        'city': 'city',
        'country': 'country'
    }

    def __init__(self, phone_number=None, number=None, prefix=None, friendly_name=None, flag=None, city=None, country=None):  # noqa: E501
        """GetPhonesResponseInner - a model defined in spec"""  # noqa: E501
        self._phone_number = None
        self._number = None
        self._prefix = None
        self._friendly_name = None
        self._flag = None
        self._city = None
        self._country = None
        self.discriminator = None
        if phone_number is not None:
            self.phone_number = phone_number
        if number is not None:
            self.number = number
        if prefix is not None:
            self.prefix = prefix
        if friendly_name is not None:
            self.friendly_name = friendly_name
        if flag is not None:
            self.flag = flag
        if city is not None:
            self.city = city
        if country is not None:
            self.country = country

    @property
    def phone_number(self):
        """Gets the phone_number of this GetPhonesResponseInner.  # noqa: E501


        :return: The phone_number of this GetPhonesResponseInner.  # noqa: E501
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """Sets the phone_number of this GetPhonesResponseInner.


        :param phone_number: The phone_number of this GetPhonesResponseInner.  # noqa: E501
        :type: str
        """

        self._phone_number = phone_number

    @property
    def number(self):
        """Gets the number of this GetPhonesResponseInner.  # noqa: E501


        :return: The number of this GetPhonesResponseInner.  # noqa: E501
        :rtype: str
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this GetPhonesResponseInner.


        :param number: The number of this GetPhonesResponseInner.  # noqa: E501
        :type: str
        """

        self._number = number

    @property
    def prefix(self):
        """Gets the prefix of this GetPhonesResponseInner.  # noqa: E501


        :return: The prefix of this GetPhonesResponseInner.  # noqa: E501
        :rtype: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """Sets the prefix of this GetPhonesResponseInner.


        :param prefix: The prefix of this GetPhonesResponseInner.  # noqa: E501
        :type: str
        """

        self._prefix = prefix

    @property
    def friendly_name(self):
        """Gets the friendly_name of this GetPhonesResponseInner.  # noqa: E501


        :return: The friendly_name of this GetPhonesResponseInner.  # noqa: E501
        :rtype: str
        """
        return self._friendly_name

    @friendly_name.setter
    def friendly_name(self, friendly_name):
        """Sets the friendly_name of this GetPhonesResponseInner.


        :param friendly_name: The friendly_name of this GetPhonesResponseInner.  # noqa: E501
        :type: str
        """

        self._friendly_name = friendly_name

    @property
    def flag(self):
        """Gets the flag of this GetPhonesResponseInner.  # noqa: E501


        :return: The flag of this GetPhonesResponseInner.  # noqa: E501
        :rtype: str
        """
        return self._flag

    @flag.setter
    def flag(self, flag):
        """Sets the flag of this GetPhonesResponseInner.


        :param flag: The flag of this GetPhonesResponseInner.  # noqa: E501
        :type: str
        """

        self._flag = flag

    @property
    def city(self):
        """Gets the city of this GetPhonesResponseInner.  # noqa: E501


        :return: The city of this GetPhonesResponseInner.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this GetPhonesResponseInner.


        :param city: The city of this GetPhonesResponseInner.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def country(self):
        """Gets the country of this GetPhonesResponseInner.  # noqa: E501


        :return: The country of this GetPhonesResponseInner.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this GetPhonesResponseInner.


        :param country: The country of this GetPhonesResponseInner.  # noqa: E501
        :type: str
        """

        self._country = country

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
        if issubclass(GetPhonesResponseInner, dict):
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
        if not isinstance(other, GetPhonesResponseInner):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
