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
from call_recorder_api.models.get_profile_response_profile import GetProfileResponseProfile  # noqa: F401,E501


class GetProfileResponse(object):
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
        'code': 'str',
        'profile': 'GetProfileResponseProfile',
        'app': 'App',
        'share_url': 'str',
        'rate_url': 'str',
        'credits': 'int',
        'credits_trans': 'int'
    }

    attribute_map = {
        'status': 'status',
        'code': 'code',
        'profile': 'profile',
        'app': 'app',
        'share_url': 'share_url',
        'rate_url': 'rate_url',
        'credits': 'credits',
        'credits_trans': 'credits_trans'
    }

    def __init__(self, status=None, code=None, profile=None, app=None, share_url=None, rate_url=None, credits=None, credits_trans=None):  # noqa: E501
        """GetProfileResponse - a model defined in spec"""  # noqa: E501
        self._status = None
        self._code = None
        self._profile = None
        self._app = None
        self._share_url = None
        self._rate_url = None
        self._credits = None
        self._credits_trans = None
        self.discriminator = None
        self.status = status
        if code is not None:
            self.code = code
        if profile is not None:
            self.profile = profile
        if app is not None:
            self.app = app
        if share_url is not None:
            self.share_url = share_url
        if rate_url is not None:
            self.rate_url = rate_url
        if credits is not None:
            self.credits = credits
        if credits_trans is not None:
            self.credits_trans = credits_trans

    @property
    def status(self):
        """Gets the status of this GetProfileResponse.  # noqa: E501


        :return: The status of this GetProfileResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this GetProfileResponse.


        :param status: The status of this GetProfileResponse.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def code(self):
        """Gets the code of this GetProfileResponse.  # noqa: E501


        :return: The code of this GetProfileResponse.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this GetProfileResponse.


        :param code: The code of this GetProfileResponse.  # noqa: E501
        :type: str
        """

        self._code = code

    @property
    def profile(self):
        """Gets the profile of this GetProfileResponse.  # noqa: E501


        :return: The profile of this GetProfileResponse.  # noqa: E501
        :rtype: GetProfileResponseProfile
        """
        return self._profile

    @profile.setter
    def profile(self, profile):
        """Sets the profile of this GetProfileResponse.


        :param profile: The profile of this GetProfileResponse.  # noqa: E501
        :type: GetProfileResponseProfile
        """

        self._profile = profile

    @property
    def app(self):
        """Gets the app of this GetProfileResponse.  # noqa: E501


        :return: The app of this GetProfileResponse.  # noqa: E501
        :rtype: App
        """
        return self._app

    @app.setter
    def app(self, app):
        """Sets the app of this GetProfileResponse.


        :param app: The app of this GetProfileResponse.  # noqa: E501
        :type: App
        """

        self._app = app

    @property
    def share_url(self):
        """Gets the share_url of this GetProfileResponse.  # noqa: E501


        :return: The share_url of this GetProfileResponse.  # noqa: E501
        :rtype: str
        """
        return self._share_url

    @share_url.setter
    def share_url(self, share_url):
        """Sets the share_url of this GetProfileResponse.


        :param share_url: The share_url of this GetProfileResponse.  # noqa: E501
        :type: str
        """

        self._share_url = share_url

    @property
    def rate_url(self):
        """Gets the rate_url of this GetProfileResponse.  # noqa: E501


        :return: The rate_url of this GetProfileResponse.  # noqa: E501
        :rtype: str
        """
        return self._rate_url

    @rate_url.setter
    def rate_url(self, rate_url):
        """Sets the rate_url of this GetProfileResponse.


        :param rate_url: The rate_url of this GetProfileResponse.  # noqa: E501
        :type: str
        """

        self._rate_url = rate_url

    @property
    def credits(self):
        """Gets the credits of this GetProfileResponse.  # noqa: E501


        :return: The credits of this GetProfileResponse.  # noqa: E501
        :rtype: int
        """
        return self._credits

    @credits.setter
    def credits(self, credits):
        """Sets the credits of this GetProfileResponse.


        :param credits: The credits of this GetProfileResponse.  # noqa: E501
        :type: int
        """

        self._credits = credits

    @property
    def credits_trans(self):
        """Gets the credits_trans of this GetProfileResponse.  # noqa: E501


        :return: The credits_trans of this GetProfileResponse.  # noqa: E501
        :rtype: int
        """
        return self._credits_trans

    @credits_trans.setter
    def credits_trans(self, credits_trans):
        """Sets the credits_trans of this GetProfileResponse.


        :param credits_trans: The credits_trans of this GetProfileResponse.  # noqa: E501
        :type: int
        """

        self._credits_trans = credits_trans

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
        if issubclass(GetProfileResponse, dict):
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
        if not isinstance(other, GetProfileResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
