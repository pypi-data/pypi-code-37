# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class UpdateStarRequest(object):
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
        'star': 'int',
        'type': 'str'
    }

    attribute_map = {
        'api_key': 'api_key',
        'id': 'id',
        'star': 'star',
        'type': 'type'
    }

    def __init__(self, api_key=None, id=None, star=None, type=None):  # noqa: E501
        """UpdateStarRequest - a model defined in spec"""  # noqa: E501
        self._api_key = None
        self._id = None
        self._star = None
        self._type = None
        self.discriminator = None
        self.api_key = api_key
        if id is not None:
            self.id = id
        if star is not None:
            self.star = star
        if type is not None:
            self.type = type

    @property
    def api_key(self):
        """Gets the api_key of this UpdateStarRequest.  # noqa: E501


        :return: The api_key of this UpdateStarRequest.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this UpdateStarRequest.


        :param api_key: The api_key of this UpdateStarRequest.  # noqa: E501
        :type: str
        """
        if api_key is None:
            raise ValueError("Invalid value for `api_key`, must not be `None`")  # noqa: E501

        self._api_key = api_key

    @property
    def id(self):
        """Gets the id of this UpdateStarRequest.  # noqa: E501


        :return: The id of this UpdateStarRequest.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UpdateStarRequest.


        :param id: The id of this UpdateStarRequest.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def star(self):
        """Gets the star of this UpdateStarRequest.  # noqa: E501


        :return: The star of this UpdateStarRequest.  # noqa: E501
        :rtype: int
        """
        return self._star

    @star.setter
    def star(self, star):
        """Sets the star of this UpdateStarRequest.


        :param star: The star of this UpdateStarRequest.  # noqa: E501
        :type: int
        """

        self._star = star

    @property
    def type(self):
        """Gets the type of this UpdateStarRequest.  # noqa: E501


        :return: The type of this UpdateStarRequest.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this UpdateStarRequest.


        :param type: The type of this UpdateStarRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["file", "folder"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if issubclass(UpdateStarRequest, dict):
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
        if not isinstance(other, UpdateStarRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
