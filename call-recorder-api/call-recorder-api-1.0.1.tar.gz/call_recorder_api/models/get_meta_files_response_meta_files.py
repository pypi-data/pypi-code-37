# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class GetMetaFilesResponseMetaFiles(object):
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
        'id': 'int',
        'parent_id': 'int',
        'name': 'str',
        'file': 'str',
        'user_id': 'int',
        'time': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'parent_id': 'parent_id',
        'name': 'name',
        'file': 'file',
        'user_id': 'user_id',
        'time': 'time'
    }

    def __init__(self, id=None, parent_id=None, name=None, file=None, user_id=None, time=None):  # noqa: E501
        """GetMetaFilesResponseMetaFiles - a model defined in spec"""  # noqa: E501
        self._id = None
        self._parent_id = None
        self._name = None
        self._file = None
        self._user_id = None
        self._time = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if parent_id is not None:
            self.parent_id = parent_id
        if name is not None:
            self.name = name
        if file is not None:
            self.file = file
        if user_id is not None:
            self.user_id = user_id
        if time is not None:
            self.time = time

    @property
    def id(self):
        """Gets the id of this GetMetaFilesResponseMetaFiles.  # noqa: E501


        :return: The id of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GetMetaFilesResponseMetaFiles.


        :param id: The id of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def parent_id(self):
        """Gets the parent_id of this GetMetaFilesResponseMetaFiles.  # noqa: E501


        :return: The parent_id of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :rtype: int
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this GetMetaFilesResponseMetaFiles.


        :param parent_id: The parent_id of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :type: int
        """

        self._parent_id = parent_id

    @property
    def name(self):
        """Gets the name of this GetMetaFilesResponseMetaFiles.  # noqa: E501


        :return: The name of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GetMetaFilesResponseMetaFiles.


        :param name: The name of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def file(self):
        """Gets the file of this GetMetaFilesResponseMetaFiles.  # noqa: E501


        :return: The file of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :rtype: str
        """
        return self._file

    @file.setter
    def file(self, file):
        """Sets the file of this GetMetaFilesResponseMetaFiles.


        :param file: The file of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :type: str
        """

        self._file = file

    @property
    def user_id(self):
        """Gets the user_id of this GetMetaFilesResponseMetaFiles.  # noqa: E501


        :return: The user_id of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :rtype: int
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this GetMetaFilesResponseMetaFiles.


        :param user_id: The user_id of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :type: int
        """

        self._user_id = user_id

    @property
    def time(self):
        """Gets the time of this GetMetaFilesResponseMetaFiles.  # noqa: E501


        :return: The time of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this GetMetaFilesResponseMetaFiles.


        :param time: The time of this GetMetaFilesResponseMetaFiles.  # noqa: E501
        :type: datetime
        """

        self._time = time

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
        if issubclass(GetMetaFilesResponseMetaFiles, dict):
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
        if not isinstance(other, GetMetaFilesResponseMetaFiles):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
