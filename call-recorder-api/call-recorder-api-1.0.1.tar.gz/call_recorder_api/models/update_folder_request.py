# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class UpdateFolderRequest(object):
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
        'name': 'str',
        '_pass': 'str',
        'is_private': 'bool'
    }

    attribute_map = {
        'api_key': 'api_key',
        'id': 'id',
        'name': 'name',
        '_pass': 'pass',
        'is_private': 'is_private'
    }

    def __init__(self, api_key=None, id=None, name=None, _pass=None, is_private=None):  # noqa: E501
        """UpdateFolderRequest - a model defined in spec"""  # noqa: E501
        self._api_key = None
        self._id = None
        self._name = None
        self.__pass = None
        self._is_private = None
        self.discriminator = None
        self.api_key = api_key
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if _pass is not None:
            self._pass = _pass
        if is_private is not None:
            self.is_private = is_private

    @property
    def api_key(self):
        """Gets the api_key of this UpdateFolderRequest.  # noqa: E501


        :return: The api_key of this UpdateFolderRequest.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this UpdateFolderRequest.


        :param api_key: The api_key of this UpdateFolderRequest.  # noqa: E501
        :type: str
        """
        if api_key is None:
            raise ValueError("Invalid value for `api_key`, must not be `None`")  # noqa: E501

        self._api_key = api_key

    @property
    def id(self):
        """Gets the id of this UpdateFolderRequest.  # noqa: E501


        :return: The id of this UpdateFolderRequest.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UpdateFolderRequest.


        :param id: The id of this UpdateFolderRequest.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this UpdateFolderRequest.  # noqa: E501


        :return: The name of this UpdateFolderRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateFolderRequest.


        :param name: The name of this UpdateFolderRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def _pass(self):
        """Gets the _pass of this UpdateFolderRequest.  # noqa: E501


        :return: The _pass of this UpdateFolderRequest.  # noqa: E501
        :rtype: str
        """
        return self.__pass

    @_pass.setter
    def _pass(self, _pass):
        """Sets the _pass of this UpdateFolderRequest.


        :param _pass: The _pass of this UpdateFolderRequest.  # noqa: E501
        :type: str
        """

        self.__pass = _pass

    @property
    def is_private(self):
        """Gets the is_private of this UpdateFolderRequest.  # noqa: E501


        :return: The is_private of this UpdateFolderRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_private

    @is_private.setter
    def is_private(self, is_private):
        """Sets the is_private of this UpdateFolderRequest.


        :param is_private: The is_private of this UpdateFolderRequest.  # noqa: E501
        :type: bool
        """

        self._is_private = is_private

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
        if issubclass(UpdateFolderRequest, dict):
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
        if not isinstance(other, UpdateFolderRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
