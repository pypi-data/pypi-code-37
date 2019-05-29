# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class GetProfileResponseProfile(object):
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
        'phone': 'str',
        'pic': 'str',
        'language': 'str',
        'is_public': 'int',
        'play_beep': 'int',
        'max_length': 'int',
        'time_zone': 'str',
        'time': 'int',
        'pin': 'str'
    }

    attribute_map = {
        'f_name': 'f_name',
        'l_name': 'l_name',
        'email': 'email',
        'phone': 'phone',
        'pic': 'pic',
        'language': 'language',
        'is_public': 'is_public',
        'play_beep': 'play_beep',
        'max_length': 'max_length',
        'time_zone': 'time_zone',
        'time': 'time',
        'pin': 'pin'
    }

    def __init__(self, f_name=None, l_name=None, email=None, phone=None, pic=None, language=None, is_public=None, play_beep=None, max_length=None, time_zone=None, time=None, pin=None):  # noqa: E501
        """GetProfileResponseProfile - a model defined in spec"""  # noqa: E501
        self._f_name = None
        self._l_name = None
        self._email = None
        self._phone = None
        self._pic = None
        self._language = None
        self._is_public = None
        self._play_beep = None
        self._max_length = None
        self._time_zone = None
        self._time = None
        self._pin = None
        self.discriminator = None
        if f_name is not None:
            self.f_name = f_name
        if l_name is not None:
            self.l_name = l_name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if pic is not None:
            self.pic = pic
        if language is not None:
            self.language = language
        if is_public is not None:
            self.is_public = is_public
        if play_beep is not None:
            self.play_beep = play_beep
        if max_length is not None:
            self.max_length = max_length
        if time_zone is not None:
            self.time_zone = time_zone
        if time is not None:
            self.time = time
        if pin is not None:
            self.pin = pin

    @property
    def f_name(self):
        """Gets the f_name of this GetProfileResponseProfile.  # noqa: E501


        :return: The f_name of this GetProfileResponseProfile.  # noqa: E501
        :rtype: str
        """
        return self._f_name

    @f_name.setter
    def f_name(self, f_name):
        """Sets the f_name of this GetProfileResponseProfile.


        :param f_name: The f_name of this GetProfileResponseProfile.  # noqa: E501
        :type: str
        """

        self._f_name = f_name

    @property
    def l_name(self):
        """Gets the l_name of this GetProfileResponseProfile.  # noqa: E501


        :return: The l_name of this GetProfileResponseProfile.  # noqa: E501
        :rtype: str
        """
        return self._l_name

    @l_name.setter
    def l_name(self, l_name):
        """Sets the l_name of this GetProfileResponseProfile.


        :param l_name: The l_name of this GetProfileResponseProfile.  # noqa: E501
        :type: str
        """

        self._l_name = l_name

    @property
    def email(self):
        """Gets the email of this GetProfileResponseProfile.  # noqa: E501


        :return: The email of this GetProfileResponseProfile.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this GetProfileResponseProfile.


        :param email: The email of this GetProfileResponseProfile.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def phone(self):
        """Gets the phone of this GetProfileResponseProfile.  # noqa: E501


        :return: The phone of this GetProfileResponseProfile.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this GetProfileResponseProfile.


        :param phone: The phone of this GetProfileResponseProfile.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def pic(self):
        """Gets the pic of this GetProfileResponseProfile.  # noqa: E501


        :return: The pic of this GetProfileResponseProfile.  # noqa: E501
        :rtype: str
        """
        return self._pic

    @pic.setter
    def pic(self, pic):
        """Sets the pic of this GetProfileResponseProfile.


        :param pic: The pic of this GetProfileResponseProfile.  # noqa: E501
        :type: str
        """

        self._pic = pic

    @property
    def language(self):
        """Gets the language of this GetProfileResponseProfile.  # noqa: E501


        :return: The language of this GetProfileResponseProfile.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this GetProfileResponseProfile.


        :param language: The language of this GetProfileResponseProfile.  # noqa: E501
        :type: str
        """

        self._language = language

    @property
    def is_public(self):
        """Gets the is_public of this GetProfileResponseProfile.  # noqa: E501


        :return: The is_public of this GetProfileResponseProfile.  # noqa: E501
        :rtype: int
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this GetProfileResponseProfile.


        :param is_public: The is_public of this GetProfileResponseProfile.  # noqa: E501
        :type: int
        """

        self._is_public = is_public

    @property
    def play_beep(self):
        """Gets the play_beep of this GetProfileResponseProfile.  # noqa: E501


        :return: The play_beep of this GetProfileResponseProfile.  # noqa: E501
        :rtype: int
        """
        return self._play_beep

    @play_beep.setter
    def play_beep(self, play_beep):
        """Sets the play_beep of this GetProfileResponseProfile.


        :param play_beep: The play_beep of this GetProfileResponseProfile.  # noqa: E501
        :type: int
        """

        self._play_beep = play_beep

    @property
    def max_length(self):
        """Gets the max_length of this GetProfileResponseProfile.  # noqa: E501


        :return: The max_length of this GetProfileResponseProfile.  # noqa: E501
        :rtype: int
        """
        return self._max_length

    @max_length.setter
    def max_length(self, max_length):
        """Sets the max_length of this GetProfileResponseProfile.


        :param max_length: The max_length of this GetProfileResponseProfile.  # noqa: E501
        :type: int
        """

        self._max_length = max_length

    @property
    def time_zone(self):
        """Gets the time_zone of this GetProfileResponseProfile.  # noqa: E501


        :return: The time_zone of this GetProfileResponseProfile.  # noqa: E501
        :rtype: str
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """Sets the time_zone of this GetProfileResponseProfile.


        :param time_zone: The time_zone of this GetProfileResponseProfile.  # noqa: E501
        :type: str
        """

        self._time_zone = time_zone

    @property
    def time(self):
        """Gets the time of this GetProfileResponseProfile.  # noqa: E501


        :return: The time of this GetProfileResponseProfile.  # noqa: E501
        :rtype: int
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this GetProfileResponseProfile.


        :param time: The time of this GetProfileResponseProfile.  # noqa: E501
        :type: int
        """

        self._time = time

    @property
    def pin(self):
        """Gets the pin of this GetProfileResponseProfile.  # noqa: E501


        :return: The pin of this GetProfileResponseProfile.  # noqa: E501
        :rtype: str
        """
        return self._pin

    @pin.setter
    def pin(self, pin):
        """Sets the pin of this GetProfileResponseProfile.


        :param pin: The pin of this GetProfileResponseProfile.  # noqa: E501
        :type: str
        """

        self._pin = pin

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
        if issubclass(GetProfileResponseProfile, dict):
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
        if not isinstance(other, GetProfileResponseProfile):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
