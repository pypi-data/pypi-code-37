# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class CreateFolderRequest(object):
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
        'name': 'str',
        '_pass': 'str'
    }

    attribute_map = {
        'api_key': 'api_key',
        'name': 'name',
        '_pass': 'pass'
    }

    def __init__(self, api_key=None, name=None, _pass=None):  # noqa: E501
        """CreateFolderRequest - a model defined in spec"""  # noqa: E501
        self._api_key = None
        self._name = None
        self.__pass = None
        self.discriminator = None
        self.api_key = api_key
        if name is not None:
            self.name = name
        if _pass is not None:
            self._pass = _pass

    @property
    def api_key(self):
        """Gets the api_key of this CreateFolderRequest.  # noqa: E501


        :return: The api_key of this CreateFolderRequest.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this CreateFolderRequest.


        :param api_key: The api_key of this CreateFolderRequest.  # noqa: E501
        :type: str
        """
        if api_key is None:
            raise ValueError("Invalid value for `api_key`, must not be `None`")  # noqa: E501

        self._api_key = api_key

    @property
    def name(self):
        """Gets the name of this CreateFolderRequest.  # noqa: E501


        :return: The name of this CreateFolderRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateFolderRequest.


        :param name: The name of this CreateFolderRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def _pass(self):
        """Gets the _pass of this CreateFolderRequest.  # noqa: E501


        :return: The _pass of this CreateFolderRequest.  # noqa: E501
        :rtype: str
        """
        return self.__pass

    @_pass.setter
    def _pass(self, _pass):
        """Sets the _pass of this CreateFolderRequest.


        :param _pass: The _pass of this CreateFolderRequest.  # noqa: E501
        :type: str
        """

        self.__pass = _pass

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
        if issubclass(CreateFolderRequest, dict):
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
        if not isinstance(other, CreateFolderRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
