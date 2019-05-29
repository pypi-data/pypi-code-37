# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class CreateFileData(object):
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
        'name': 'str',
        'email': 'str',
        'phone': 'str',
        'l_name': 'str',
        'f_name': 'str',
        'notes': 'str',
        'tags': 'str',
        'meta': 'list[str]',
        'source': 'str',
        'remind_days': 'str',
        'remind_date': 'datetime'
    }

    attribute_map = {
        'name': 'name',
        'email': 'email',
        'phone': 'phone',
        'l_name': 'l_name',
        'f_name': 'f_name',
        'notes': 'notes',
        'tags': 'tags',
        'meta': 'meta',
        'source': 'source',
        'remind_days': 'remind_days',
        'remind_date': 'remind_date'
    }

    def __init__(self, name=None, email=None, phone=None, l_name=None, f_name=None, notes=None, tags=None, meta=None, source=None, remind_days=None, remind_date=None):  # noqa: E501
        """CreateFileData - a model defined in spec"""  # noqa: E501
        self._name = None
        self._email = None
        self._phone = None
        self._l_name = None
        self._f_name = None
        self._notes = None
        self._tags = None
        self._meta = None
        self._source = None
        self._remind_days = None
        self._remind_date = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if l_name is not None:
            self.l_name = l_name
        if f_name is not None:
            self.f_name = f_name
        if notes is not None:
            self.notes = notes
        if tags is not None:
            self.tags = tags
        if meta is not None:
            self.meta = meta
        if source is not None:
            self.source = source
        if remind_days is not None:
            self.remind_days = remind_days
        if remind_date is not None:
            self.remind_date = remind_date

    @property
    def name(self):
        """Gets the name of this CreateFileData.  # noqa: E501


        :return: The name of this CreateFileData.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateFileData.


        :param name: The name of this CreateFileData.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def email(self):
        """Gets the email of this CreateFileData.  # noqa: E501


        :return: The email of this CreateFileData.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this CreateFileData.


        :param email: The email of this CreateFileData.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def phone(self):
        """Gets the phone of this CreateFileData.  # noqa: E501


        :return: The phone of this CreateFileData.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this CreateFileData.


        :param phone: The phone of this CreateFileData.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def l_name(self):
        """Gets the l_name of this CreateFileData.  # noqa: E501


        :return: The l_name of this CreateFileData.  # noqa: E501
        :rtype: str
        """
        return self._l_name

    @l_name.setter
    def l_name(self, l_name):
        """Sets the l_name of this CreateFileData.


        :param l_name: The l_name of this CreateFileData.  # noqa: E501
        :type: str
        """

        self._l_name = l_name

    @property
    def f_name(self):
        """Gets the f_name of this CreateFileData.  # noqa: E501


        :return: The f_name of this CreateFileData.  # noqa: E501
        :rtype: str
        """
        return self._f_name

    @f_name.setter
    def f_name(self, f_name):
        """Sets the f_name of this CreateFileData.


        :param f_name: The f_name of this CreateFileData.  # noqa: E501
        :type: str
        """

        self._f_name = f_name

    @property
    def notes(self):
        """Gets the notes of this CreateFileData.  # noqa: E501


        :return: The notes of this CreateFileData.  # noqa: E501
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this CreateFileData.


        :param notes: The notes of this CreateFileData.  # noqa: E501
        :type: str
        """

        self._notes = notes

    @property
    def tags(self):
        """Gets the tags of this CreateFileData.  # noqa: E501


        :return: The tags of this CreateFileData.  # noqa: E501
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreateFileData.


        :param tags: The tags of this CreateFileData.  # noqa: E501
        :type: str
        """

        self._tags = tags

    @property
    def meta(self):
        """Gets the meta of this CreateFileData.  # noqa: E501


        :return: The meta of this CreateFileData.  # noqa: E501
        :rtype: list[str]
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """Sets the meta of this CreateFileData.


        :param meta: The meta of this CreateFileData.  # noqa: E501
        :type: list[str]
        """

        self._meta = meta

    @property
    def source(self):
        """Gets the source of this CreateFileData.  # noqa: E501


        :return: The source of this CreateFileData.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this CreateFileData.


        :param source: The source of this CreateFileData.  # noqa: E501
        :type: str
        """
        allowed_values = ["0", "1"]  # noqa: E501
        if source not in allowed_values:
            raise ValueError(
                "Invalid value for `source` ({0}), must be one of {1}"  # noqa: E501
                .format(source, allowed_values)
            )

        self._source = source

    @property
    def remind_days(self):
        """Gets the remind_days of this CreateFileData.  # noqa: E501


        :return: The remind_days of this CreateFileData.  # noqa: E501
        :rtype: str
        """
        return self._remind_days

    @remind_days.setter
    def remind_days(self, remind_days):
        """Sets the remind_days of this CreateFileData.


        :param remind_days: The remind_days of this CreateFileData.  # noqa: E501
        :type: str
        """

        self._remind_days = remind_days

    @property
    def remind_date(self):
        """Gets the remind_date of this CreateFileData.  # noqa: E501


        :return: The remind_date of this CreateFileData.  # noqa: E501
        :rtype: datetime
        """
        return self._remind_date

    @remind_date.setter
    def remind_date(self, remind_date):
        """Sets the remind_date of this CreateFileData.


        :param remind_date: The remind_date of this CreateFileData.  # noqa: E501
        :type: datetime
        """

        self._remind_date = remind_date

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
        if issubclass(CreateFileData, dict):
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
        if not isinstance(other, CreateFileData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
