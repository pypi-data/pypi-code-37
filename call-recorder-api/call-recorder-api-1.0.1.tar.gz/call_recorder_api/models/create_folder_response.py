# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class CreateFolderResponse(object):
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
        'status': 'str',
        'msg': 'str',
        'id': 'int',
        'code': 'str'
    }

    attribute_map = {
        'status': 'status',
        'msg': 'msg',
        'id': 'id',
        'code': 'code'
    }

    def __init__(self, status=None, msg=None, id=None, code=None):  # noqa: E501
        """CreateFolderResponse - a model defined in spec"""  # noqa: E501
        self._status = None
        self._msg = None
        self._id = None
        self._code = None
        self.discriminator = None
        self.status = status
        if msg is not None:
            self.msg = msg
        if id is not None:
            self.id = id
        if code is not None:
            self.code = code

    @property
    def status(self):
        """Gets the status of this CreateFolderResponse.  # noqa: E501


        :return: The status of this CreateFolderResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this CreateFolderResponse.


        :param status: The status of this CreateFolderResponse.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def msg(self):
        """Gets the msg of this CreateFolderResponse.  # noqa: E501


        :return: The msg of this CreateFolderResponse.  # noqa: E501
        :rtype: str
        """
        return self._msg

    @msg.setter
    def msg(self, msg):
        """Sets the msg of this CreateFolderResponse.


        :param msg: The msg of this CreateFolderResponse.  # noqa: E501
        :type: str
        """

        self._msg = msg

    @property
    def id(self):
        """Gets the id of this CreateFolderResponse.  # noqa: E501


        :return: The id of this CreateFolderResponse.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CreateFolderResponse.


        :param id: The id of this CreateFolderResponse.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def code(self):
        """Gets the code of this CreateFolderResponse.  # noqa: E501


        :return: The code of this CreateFolderResponse.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this CreateFolderResponse.


        :param code: The code of this CreateFolderResponse.  # noqa: E501
        :type: str
        """

        self._code = code

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
        if issubclass(CreateFolderResponse, dict):
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
        if not isinstance(other, CreateFolderResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
