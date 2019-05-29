# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six
from call_recorder_api.models.get_files_response_files import GetFilesResponseFiles  # noqa: F401,E501


class GetFilesResponse(object):
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
        'credits': 'int',
        'credits_trans': 'int',
        'files': 'list[GetFilesResponseFiles]'
    }

    attribute_map = {
        'status': 'status',
        'credits': 'credits',
        'credits_trans': 'credits_trans',
        'files': 'files'
    }

    def __init__(self, status=None, credits=None, credits_trans=None, files=None):  # noqa: E501
        """GetFilesResponse - a model defined in spec"""  # noqa: E501
        self._status = None
        self._credits = None
        self._credits_trans = None
        self._files = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if credits is not None:
            self.credits = credits
        if credits_trans is not None:
            self.credits_trans = credits_trans
        if files is not None:
            self.files = files

    @property
    def status(self):
        """Gets the status of this GetFilesResponse.  # noqa: E501


        :return: The status of this GetFilesResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this GetFilesResponse.


        :param status: The status of this GetFilesResponse.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def credits(self):
        """Gets the credits of this GetFilesResponse.  # noqa: E501


        :return: The credits of this GetFilesResponse.  # noqa: E501
        :rtype: int
        """
        return self._credits

    @credits.setter
    def credits(self, credits):
        """Sets the credits of this GetFilesResponse.


        :param credits: The credits of this GetFilesResponse.  # noqa: E501
        :type: int
        """

        self._credits = credits

    @property
    def credits_trans(self):
        """Gets the credits_trans of this GetFilesResponse.  # noqa: E501


        :return: The credits_trans of this GetFilesResponse.  # noqa: E501
        :rtype: int
        """
        return self._credits_trans

    @credits_trans.setter
    def credits_trans(self, credits_trans):
        """Sets the credits_trans of this GetFilesResponse.


        :param credits_trans: The credits_trans of this GetFilesResponse.  # noqa: E501
        :type: int
        """

        self._credits_trans = credits_trans

    @property
    def files(self):
        """Gets the files of this GetFilesResponse.  # noqa: E501


        :return: The files of this GetFilesResponse.  # noqa: E501
        :rtype: list[GetFilesResponseFiles]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this GetFilesResponse.


        :param files: The files of this GetFilesResponse.  # noqa: E501
        :type: list[GetFilesResponseFiles]
        """

        self._files = files

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
        if issubclass(GetFilesResponse, dict):
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
        if not isinstance(other, GetFilesResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
