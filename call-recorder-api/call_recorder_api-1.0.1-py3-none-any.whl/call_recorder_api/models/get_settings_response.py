# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six
from call_recorder_api.models.app import App  # noqa: F401,E501
from call_recorder_api.models.get_settings_response_settings import GetSettingsResponseSettings  # noqa: F401,E501


class GetSettingsResponse(object):
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
        'app': 'App',
        'credits': 'int',
        'settings': 'GetSettingsResponseSettings'
    }

    attribute_map = {
        'status': 'status',
        'app': 'app',
        'credits': 'credits',
        'settings': 'settings'
    }

    def __init__(self, status=None, app=None, credits=None, settings=None):  # noqa: E501
        """GetSettingsResponse - a model defined in spec"""  # noqa: E501
        self._status = None
        self._app = None
        self._credits = None
        self._settings = None
        self.discriminator = None
        self.status = status
        if app is not None:
            self.app = app
        if credits is not None:
            self.credits = credits
        if settings is not None:
            self.settings = settings

    @property
    def status(self):
        """Gets the status of this GetSettingsResponse.  # noqa: E501


        :return: The status of this GetSettingsResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this GetSettingsResponse.


        :param status: The status of this GetSettingsResponse.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def app(self):
        """Gets the app of this GetSettingsResponse.  # noqa: E501


        :return: The app of this GetSettingsResponse.  # noqa: E501
        :rtype: App
        """
        return self._app

    @app.setter
    def app(self, app):
        """Sets the app of this GetSettingsResponse.


        :param app: The app of this GetSettingsResponse.  # noqa: E501
        :type: App
        """

        self._app = app

    @property
    def credits(self):
        """Gets the credits of this GetSettingsResponse.  # noqa: E501


        :return: The credits of this GetSettingsResponse.  # noqa: E501
        :rtype: int
        """
        return self._credits

    @credits.setter
    def credits(self, credits):
        """Sets the credits of this GetSettingsResponse.


        :param credits: The credits of this GetSettingsResponse.  # noqa: E501
        :type: int
        """

        self._credits = credits

    @property
    def settings(self):
        """Gets the settings of this GetSettingsResponse.  # noqa: E501


        :return: The settings of this GetSettingsResponse.  # noqa: E501
        :rtype: GetSettingsResponseSettings
        """
        return self._settings

    @settings.setter
    def settings(self, settings):
        """Sets the settings of this GetSettingsResponse.


        :param settings: The settings of this GetSettingsResponse.  # noqa: E501
        :type: GetSettingsResponseSettings
        """

        self._settings = settings

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
        if issubclass(GetSettingsResponse, dict):
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
        if not isinstance(other, GetSettingsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
