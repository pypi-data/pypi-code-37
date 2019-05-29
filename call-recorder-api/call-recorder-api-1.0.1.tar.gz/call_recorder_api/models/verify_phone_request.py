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
from call_recorder_api.models.device_type import DeviceType  # noqa: F401,E501


class VerifyPhoneRequest(object):
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
        'token': 'str',
        'phone': 'str',
        'code': 'str',
        'mcc': 'str',
        'app': 'App',
        'device_token': 'str',
        'device_id': 'str',
        'device_type': 'DeviceType',
        'time_zone': 'str'
    }

    attribute_map = {
        'token': 'token',
        'phone': 'phone',
        'code': 'code',
        'mcc': 'mcc',
        'app': 'app',
        'device_token': 'device_token',
        'device_id': 'device_id',
        'device_type': 'device_type',
        'time_zone': 'time_zone'
    }

    def __init__(self, token=None, phone=None, code=None, mcc=None, app=None, device_token=None, device_id=None, device_type=None, time_zone=None):  # noqa: E501
        """VerifyPhoneRequest - a model defined in spec"""  # noqa: E501
        self._token = None
        self._phone = None
        self._code = None
        self._mcc = None
        self._app = None
        self._device_token = None
        self._device_id = None
        self._device_type = None
        self._time_zone = None
        self.discriminator = None
        self.token = token
        self.phone = phone
        self.code = code
        self.mcc = mcc
        self.app = app
        self.device_token = device_token
        if device_id is not None:
            self.device_id = device_id
        self.device_type = device_type
        self.time_zone = time_zone

    @property
    def token(self):
        """Gets the token of this VerifyPhoneRequest.  # noqa: E501


        :return: The token of this VerifyPhoneRequest.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this VerifyPhoneRequest.


        :param token: The token of this VerifyPhoneRequest.  # noqa: E501
        :type: str
        """
        if token is None:
            raise ValueError("Invalid value for `token`, must not be `None`")  # noqa: E501

        self._token = token

    @property
    def phone(self):
        """Gets the phone of this VerifyPhoneRequest.  # noqa: E501


        :return: The phone of this VerifyPhoneRequest.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this VerifyPhoneRequest.


        :param phone: The phone of this VerifyPhoneRequest.  # noqa: E501
        :type: str
        """
        if phone is None:
            raise ValueError("Invalid value for `phone`, must not be `None`")  # noqa: E501

        self._phone = phone

    @property
    def code(self):
        """Gets the code of this VerifyPhoneRequest.  # noqa: E501


        :return: The code of this VerifyPhoneRequest.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this VerifyPhoneRequest.


        :param code: The code of this VerifyPhoneRequest.  # noqa: E501
        :type: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501

        self._code = code

    @property
    def mcc(self):
        """Gets the mcc of this VerifyPhoneRequest.  # noqa: E501


        :return: The mcc of this VerifyPhoneRequest.  # noqa: E501
        :rtype: str
        """
        return self._mcc

    @mcc.setter
    def mcc(self, mcc):
        """Sets the mcc of this VerifyPhoneRequest.


        :param mcc: The mcc of this VerifyPhoneRequest.  # noqa: E501
        :type: str
        """
        if mcc is None:
            raise ValueError("Invalid value for `mcc`, must not be `None`")  # noqa: E501

        self._mcc = mcc

    @property
    def app(self):
        """Gets the app of this VerifyPhoneRequest.  # noqa: E501


        :return: The app of this VerifyPhoneRequest.  # noqa: E501
        :rtype: App
        """
        return self._app

    @app.setter
    def app(self, app):
        """Sets the app of this VerifyPhoneRequest.


        :param app: The app of this VerifyPhoneRequest.  # noqa: E501
        :type: App
        """
        if app is None:
            raise ValueError("Invalid value for `app`, must not be `None`")  # noqa: E501

        self._app = app

    @property
    def device_token(self):
        """Gets the device_token of this VerifyPhoneRequest.  # noqa: E501


        :return: The device_token of this VerifyPhoneRequest.  # noqa: E501
        :rtype: str
        """
        return self._device_token

    @device_token.setter
    def device_token(self, device_token):
        """Sets the device_token of this VerifyPhoneRequest.


        :param device_token: The device_token of this VerifyPhoneRequest.  # noqa: E501
        :type: str
        """
        if device_token is None:
            raise ValueError("Invalid value for `device_token`, must not be `None`")  # noqa: E501

        self._device_token = device_token

    @property
    def device_id(self):
        """Gets the device_id of this VerifyPhoneRequest.  # noqa: E501


        :return: The device_id of this VerifyPhoneRequest.  # noqa: E501
        :rtype: str
        """
        return self._device_id

    @device_id.setter
    def device_id(self, device_id):
        """Sets the device_id of this VerifyPhoneRequest.


        :param device_id: The device_id of this VerifyPhoneRequest.  # noqa: E501
        :type: str
        """

        self._device_id = device_id

    @property
    def device_type(self):
        """Gets the device_type of this VerifyPhoneRequest.  # noqa: E501


        :return: The device_type of this VerifyPhoneRequest.  # noqa: E501
        :rtype: DeviceType
        """
        return self._device_type

    @device_type.setter
    def device_type(self, device_type):
        """Sets the device_type of this VerifyPhoneRequest.


        :param device_type: The device_type of this VerifyPhoneRequest.  # noqa: E501
        :type: DeviceType
        """
        if device_type is None:
            raise ValueError("Invalid value for `device_type`, must not be `None`")  # noqa: E501

        self._device_type = device_type

    @property
    def time_zone(self):
        """Gets the time_zone of this VerifyPhoneRequest.  # noqa: E501


        :return: The time_zone of this VerifyPhoneRequest.  # noqa: E501
        :rtype: str
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """Sets the time_zone of this VerifyPhoneRequest.


        :param time_zone: The time_zone of this VerifyPhoneRequest.  # noqa: E501
        :type: str
        """
        if time_zone is None:
            raise ValueError("Invalid value for `time_zone`, must not be `None`")  # noqa: E501

        self._time_zone = time_zone

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
        if issubclass(VerifyPhoneRequest, dict):
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
        if not isinstance(other, VerifyPhoneRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
