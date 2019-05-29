# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class GetMessagesResponseMsgs(object):
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
        'title': 'str',
        'body': 'str',
        'time': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'title': 'title',
        'body': 'body',
        'time': 'time'
    }

    def __init__(self, id=None, title=None, body=None, time=None):  # noqa: E501
        """GetMessagesResponseMsgs - a model defined in spec"""  # noqa: E501
        self._id = None
        self._title = None
        self._body = None
        self._time = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if title is not None:
            self.title = title
        if body is not None:
            self.body = body
        if time is not None:
            self.time = time

    @property
    def id(self):
        """Gets the id of this GetMessagesResponseMsgs.  # noqa: E501


        :return: The id of this GetMessagesResponseMsgs.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GetMessagesResponseMsgs.


        :param id: The id of this GetMessagesResponseMsgs.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def title(self):
        """Gets the title of this GetMessagesResponseMsgs.  # noqa: E501


        :return: The title of this GetMessagesResponseMsgs.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this GetMessagesResponseMsgs.


        :param title: The title of this GetMessagesResponseMsgs.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def body(self):
        """Gets the body of this GetMessagesResponseMsgs.  # noqa: E501


        :return: The body of this GetMessagesResponseMsgs.  # noqa: E501
        :rtype: str
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this GetMessagesResponseMsgs.


        :param body: The body of this GetMessagesResponseMsgs.  # noqa: E501
        :type: str
        """

        self._body = body

    @property
    def time(self):
        """Gets the time of this GetMessagesResponseMsgs.  # noqa: E501


        :return: The time of this GetMessagesResponseMsgs.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this GetMessagesResponseMsgs.


        :param time: The time of this GetMessagesResponseMsgs.  # noqa: E501
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
        if issubclass(GetMessagesResponseMsgs, dict):
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
        if not isinstance(other, GetMessagesResponseMsgs):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
