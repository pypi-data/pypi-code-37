# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class GetFoldersResponseFolders(object):
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
        'name': 'str',
        'created': 'int',
        'updated': 'int',
        'is_start': 'int',
        'order_id': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'created': 'created',
        'updated': 'updated',
        'is_start': 'is_start',
        'order_id': 'order_id'
    }

    def __init__(self, id=None, name=None, created=None, updated=None, is_start=None, order_id=None):  # noqa: E501
        """GetFoldersResponseFolders - a model defined in spec"""  # noqa: E501
        self._id = None
        self._name = None
        self._created = None
        self._updated = None
        self._is_start = None
        self._order_id = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated
        if is_start is not None:
            self.is_start = is_start
        if order_id is not None:
            self.order_id = order_id

    @property
    def id(self):
        """Gets the id of this GetFoldersResponseFolders.  # noqa: E501


        :return: The id of this GetFoldersResponseFolders.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GetFoldersResponseFolders.


        :param id: The id of this GetFoldersResponseFolders.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this GetFoldersResponseFolders.  # noqa: E501


        :return: The name of this GetFoldersResponseFolders.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GetFoldersResponseFolders.


        :param name: The name of this GetFoldersResponseFolders.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def created(self):
        """Gets the created of this GetFoldersResponseFolders.  # noqa: E501


        :return: The created of this GetFoldersResponseFolders.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this GetFoldersResponseFolders.


        :param created: The created of this GetFoldersResponseFolders.  # noqa: E501
        :type: int
        """

        self._created = created

    @property
    def updated(self):
        """Gets the updated of this GetFoldersResponseFolders.  # noqa: E501


        :return: The updated of this GetFoldersResponseFolders.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this GetFoldersResponseFolders.


        :param updated: The updated of this GetFoldersResponseFolders.  # noqa: E501
        :type: int
        """

        self._updated = updated

    @property
    def is_start(self):
        """Gets the is_start of this GetFoldersResponseFolders.  # noqa: E501


        :return: The is_start of this GetFoldersResponseFolders.  # noqa: E501
        :rtype: int
        """
        return self._is_start

    @is_start.setter
    def is_start(self, is_start):
        """Sets the is_start of this GetFoldersResponseFolders.


        :param is_start: The is_start of this GetFoldersResponseFolders.  # noqa: E501
        :type: int
        """

        self._is_start = is_start

    @property
    def order_id(self):
        """Gets the order_id of this GetFoldersResponseFolders.  # noqa: E501


        :return: The order_id of this GetFoldersResponseFolders.  # noqa: E501
        :rtype: int
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this GetFoldersResponseFolders.


        :param order_id: The order_id of this GetFoldersResponseFolders.  # noqa: E501
        :type: int
        """

        self._order_id = order_id

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
        if issubclass(GetFoldersResponseFolders, dict):
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
        if not isinstance(other, GetFoldersResponseFolders):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
