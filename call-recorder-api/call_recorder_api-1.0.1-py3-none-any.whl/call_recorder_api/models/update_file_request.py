# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class UpdateFileRequest(object):
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
        'id': 'int',
        'f_name': 'str',
        'l_name': 'str',
        'notes': 'str',
        'email': 'str',
        'phone': 'str',
        'tags': 'str',
        'folder_id': 'int',
        'name': 'str',
        'remind_days': 'str',
        'remind_date': 'datetime'
    }

    attribute_map = {
        'api_key': 'api_key',
        'id': 'id',
        'f_name': 'f_name',
        'l_name': 'l_name',
        'notes': 'notes',
        'email': 'email',
        'phone': 'phone',
        'tags': 'tags',
        'folder_id': 'folder_id',
        'name': 'name',
        'remind_days': 'remind_days',
        'remind_date': 'remind_date'
    }

    def __init__(self, api_key=None, id=None, f_name=None, l_name=None, notes=None, email=None, phone=None, tags=None, folder_id=None, name=None, remind_days=None, remind_date=None):  # noqa: E501
        """UpdateFileRequest - a model defined in spec"""  # noqa: E501
        self._api_key = None
        self._id = None
        self._f_name = None
        self._l_name = None
        self._notes = None
        self._email = None
        self._phone = None
        self._tags = None
        self._folder_id = None
        self._name = None
        self._remind_days = None
        self._remind_date = None
        self.discriminator = None
        self.api_key = api_key
        if id is not None:
            self.id = id
        if f_name is not None:
            self.f_name = f_name
        if l_name is not None:
            self.l_name = l_name
        if notes is not None:
            self.notes = notes
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if tags is not None:
            self.tags = tags
        if folder_id is not None:
            self.folder_id = folder_id
        if name is not None:
            self.name = name
        if remind_days is not None:
            self.remind_days = remind_days
        if remind_date is not None:
            self.remind_date = remind_date

    @property
    def api_key(self):
        """Gets the api_key of this UpdateFileRequest.  # noqa: E501


        :return: The api_key of this UpdateFileRequest.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this UpdateFileRequest.


        :param api_key: The api_key of this UpdateFileRequest.  # noqa: E501
        :type: str
        """
        if api_key is None:
            raise ValueError("Invalid value for `api_key`, must not be `None`")  # noqa: E501

        self._api_key = api_key

    @property
    def id(self):
        """Gets the id of this UpdateFileRequest.  # noqa: E501


        :return: The id of this UpdateFileRequest.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UpdateFileRequest.


        :param id: The id of this UpdateFileRequest.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def f_name(self):
        """Gets the f_name of this UpdateFileRequest.  # noqa: E501


        :return: The f_name of this UpdateFileRequest.  # noqa: E501
        :rtype: str
        """
        return self._f_name

    @f_name.setter
    def f_name(self, f_name):
        """Sets the f_name of this UpdateFileRequest.


        :param f_name: The f_name of this UpdateFileRequest.  # noqa: E501
        :type: str
        """

        self._f_name = f_name

    @property
    def l_name(self):
        """Gets the l_name of this UpdateFileRequest.  # noqa: E501


        :return: The l_name of this UpdateFileRequest.  # noqa: E501
        :rtype: str
        """
        return self._l_name

    @l_name.setter
    def l_name(self, l_name):
        """Sets the l_name of this UpdateFileRequest.


        :param l_name: The l_name of this UpdateFileRequest.  # noqa: E501
        :type: str
        """

        self._l_name = l_name

    @property
    def notes(self):
        """Gets the notes of this UpdateFileRequest.  # noqa: E501


        :return: The notes of this UpdateFileRequest.  # noqa: E501
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this UpdateFileRequest.


        :param notes: The notes of this UpdateFileRequest.  # noqa: E501
        :type: str
        """

        self._notes = notes

    @property
    def email(self):
        """Gets the email of this UpdateFileRequest.  # noqa: E501


        :return: The email of this UpdateFileRequest.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UpdateFileRequest.


        :param email: The email of this UpdateFileRequest.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def phone(self):
        """Gets the phone of this UpdateFileRequest.  # noqa: E501


        :return: The phone of this UpdateFileRequest.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this UpdateFileRequest.


        :param phone: The phone of this UpdateFileRequest.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def tags(self):
        """Gets the tags of this UpdateFileRequest.  # noqa: E501


        :return: The tags of this UpdateFileRequest.  # noqa: E501
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this UpdateFileRequest.


        :param tags: The tags of this UpdateFileRequest.  # noqa: E501
        :type: str
        """

        self._tags = tags

    @property
    def folder_id(self):
        """Gets the folder_id of this UpdateFileRequest.  # noqa: E501


        :return: The folder_id of this UpdateFileRequest.  # noqa: E501
        :rtype: int
        """
        return self._folder_id

    @folder_id.setter
    def folder_id(self, folder_id):
        """Sets the folder_id of this UpdateFileRequest.


        :param folder_id: The folder_id of this UpdateFileRequest.  # noqa: E501
        :type: int
        """

        self._folder_id = folder_id

    @property
    def name(self):
        """Gets the name of this UpdateFileRequest.  # noqa: E501


        :return: The name of this UpdateFileRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateFileRequest.


        :param name: The name of this UpdateFileRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def remind_days(self):
        """Gets the remind_days of this UpdateFileRequest.  # noqa: E501


        :return: The remind_days of this UpdateFileRequest.  # noqa: E501
        :rtype: str
        """
        return self._remind_days

    @remind_days.setter
    def remind_days(self, remind_days):
        """Sets the remind_days of this UpdateFileRequest.


        :param remind_days: The remind_days of this UpdateFileRequest.  # noqa: E501
        :type: str
        """

        self._remind_days = remind_days

    @property
    def remind_date(self):
        """Gets the remind_date of this UpdateFileRequest.  # noqa: E501


        :return: The remind_date of this UpdateFileRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._remind_date

    @remind_date.setter
    def remind_date(self, remind_date):
        """Sets the remind_date of this UpdateFileRequest.


        :param remind_date: The remind_date of this UpdateFileRequest.  # noqa: E501
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
        if issubclass(UpdateFileRequest, dict):
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
        if not isinstance(other, UpdateFileRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
