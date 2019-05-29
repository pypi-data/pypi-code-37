# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six
from call_recorder_api.models.get_meta_files_response_meta_files import GetMetaFilesResponseMetaFiles  # noqa: F401,E501


class GetMetaFilesResponse(object):
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
        'meta_files': 'list[GetMetaFilesResponseMetaFiles]'
    }

    attribute_map = {
        'status': 'status',
        'meta_files': 'meta_files'
    }

    def __init__(self, status=None, meta_files=None):  # noqa: E501
        """GetMetaFilesResponse - a model defined in spec"""  # noqa: E501
        self._status = None
        self._meta_files = None
        self.discriminator = None
        self.status = status
        if meta_files is not None:
            self.meta_files = meta_files

    @property
    def status(self):
        """Gets the status of this GetMetaFilesResponse.  # noqa: E501


        :return: The status of this GetMetaFilesResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this GetMetaFilesResponse.


        :param status: The status of this GetMetaFilesResponse.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def meta_files(self):
        """Gets the meta_files of this GetMetaFilesResponse.  # noqa: E501


        :return: The meta_files of this GetMetaFilesResponse.  # noqa: E501
        :rtype: list[GetMetaFilesResponseMetaFiles]
        """
        return self._meta_files

    @meta_files.setter
    def meta_files(self, meta_files):
        """Sets the meta_files of this GetMetaFilesResponse.


        :param meta_files: The meta_files of this GetMetaFilesResponse.  # noqa: E501
        :type: list[GetMetaFilesResponseMetaFiles]
        """

        self._meta_files = meta_files

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
        if issubclass(GetMetaFilesResponse, dict):
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
        if not isinstance(other, GetMetaFilesResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
