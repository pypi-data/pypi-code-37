# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class FolderOrder(object):
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
        'order_id': 'int'
    }

    attribute_map = {
        'id': 'id',
        'order_id': 'order_id'
    }

    def __init__(self, id=None, order_id=None):  # noqa: E501
        """FolderOrder - a model defined in spec"""  # noqa: E501
        self._id = None
        self._order_id = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if order_id is not None:
            self.order_id = order_id

    @property
    def id(self):
        """Gets the id of this FolderOrder.  # noqa: E501


        :return: The id of this FolderOrder.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FolderOrder.


        :param id: The id of this FolderOrder.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def order_id(self):
        """Gets the order_id of this FolderOrder.  # noqa: E501


        :return: The order_id of this FolderOrder.  # noqa: E501
        :rtype: int
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this FolderOrder.


        :param order_id: The order_id of this FolderOrder.  # noqa: E501
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
        if issubclass(FolderOrder, dict):
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
        if not isinstance(other, FolderOrder):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other


class UpdateOrderRequest(object):
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
        'folders': 'list[FolderOrder]'
    }

    attribute_map = {
        'api_key': 'api_key',
        'folders': 'folders'
    }

    def __init__(self, api_key=None, folders=None):  # noqa: E501
        """UpdateOrderRequest - a model defined in spec"""  # noqa: E501
        self._api_key = None
        self._folders = None
        self.discriminator = None
        self.api_key = api_key
        if folders is not None:
            self.folders = folders

    @property
    def api_key(self):
        """Gets the api_key of this UpdateOrderRequest.  # noqa: E501


        :return: The api_key of this UpdateOrderRequest.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this UpdateOrderRequest.


        :param api_key: The api_key of this UpdateOrderRequest.  # noqa: E501
        :type: str
        """
        if api_key is None:
            raise ValueError("Invalid value for `api_key`, must not be `None`")  # noqa: E501

        self._api_key = api_key

    @property
    def folders(self):
        """Gets the folders of this UpdateOrderRequest.  # noqa: E501


        :return: The folders of this UpdateOrderRequest.  # noqa: E501
        :rtype: list[FolderOrder]
        """
        return self._folders

    @folders.setter
    def folders(self, folders):
        """Sets the folders of this UpdateOrderRequest.


        :param folders: The folders of this UpdateOrderRequest.  # noqa: E501
        :type: list[FolderOrder]
        """

        self._folders = folders

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
        if issubclass(UpdateOrderRequest, dict):
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
        if not isinstance(other, UpdateOrderRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
