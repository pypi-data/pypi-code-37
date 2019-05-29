# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six
from call_recorder_api.models.files_permission import FilesPermission  # noqa: F401,E501
from call_recorder_api.models.play_beep import PlayBeep  # noqa: F401,E501


class GetSettingsResponseSettings(object):
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
        'play_beep': 'PlayBeep',
        'files_permission': 'FilesPermission'
    }

    attribute_map = {
        'play_beep': 'play_beep',
        'files_permission': 'files_permission'
    }

    def __init__(self, play_beep=None, files_permission=None):  # noqa: E501
        """GetSettingsResponseSettings - a model defined in spec"""  # noqa: E501
        self._play_beep = None
        self._files_permission = None
        self.discriminator = None
        if play_beep is not None:
            self.play_beep = play_beep
        if files_permission is not None:
            self.files_permission = files_permission

    @property
    def play_beep(self):
        """Gets the play_beep of this GetSettingsResponseSettings.  # noqa: E501


        :return: The play_beep of this GetSettingsResponseSettings.  # noqa: E501
        :rtype: PlayBeep
        """
        return self._play_beep

    @play_beep.setter
    def play_beep(self, play_beep):
        """Sets the play_beep of this GetSettingsResponseSettings.


        :param play_beep: The play_beep of this GetSettingsResponseSettings.  # noqa: E501
        :type: PlayBeep
        """

        self._play_beep = play_beep

    @property
    def files_permission(self):
        """Gets the files_permission of this GetSettingsResponseSettings.  # noqa: E501


        :return: The files_permission of this GetSettingsResponseSettings.  # noqa: E501
        :rtype: FilesPermission
        """
        return self._files_permission

    @files_permission.setter
    def files_permission(self, files_permission):
        """Sets the files_permission of this GetSettingsResponseSettings.


        :param files_permission: The files_permission of this GetSettingsResponseSettings.  # noqa: E501
        :type: FilesPermission
        """

        self._files_permission = files_permission

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
        if issubclass(GetSettingsResponseSettings, dict):
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
        if not isinstance(other, GetSettingsResponseSettings):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
