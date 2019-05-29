# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six
from call_recorder_api.models.device_type import DeviceType  # noqa: F401,E501


class BuyCreditsRequest(object):
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
        'amount': 'int',
        'receipt': 'str',
        'product_id': 'int',
        'device_type': 'DeviceType'
    }

    attribute_map = {
        'api_key': 'api_key',
        'amount': 'amount',
        'receipt': 'receipt',
        'product_id': 'product_id',
        'device_type': 'device_type'
    }

    def __init__(self, api_key=None, amount=None, receipt=None, product_id=None, device_type=None):  # noqa: E501
        """BuyCreditsRequest - a model defined in spec"""  # noqa: E501
        self._api_key = None
        self._amount = None
        self._receipt = None
        self._product_id = None
        self._device_type = None
        self.discriminator = None
        self.api_key = api_key
        if amount is not None:
            self.amount = amount
        if receipt is not None:
            self.receipt = receipt
        if product_id is not None:
            self.product_id = product_id
        if device_type is not None:
            self.device_type = device_type

    @property
    def api_key(self):
        """Gets the api_key of this BuyCreditsRequest.  # noqa: E501


        :return: The api_key of this BuyCreditsRequest.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this BuyCreditsRequest.


        :param api_key: The api_key of this BuyCreditsRequest.  # noqa: E501
        :type: str
        """
        if api_key is None:
            raise ValueError("Invalid value for `api_key`, must not be `None`")  # noqa: E501

        self._api_key = api_key

    @property
    def amount(self):
        """Gets the amount of this BuyCreditsRequest.  # noqa: E501


        :return: The amount of this BuyCreditsRequest.  # noqa: E501
        :rtype: int
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this BuyCreditsRequest.


        :param amount: The amount of this BuyCreditsRequest.  # noqa: E501
        :type: int
        """

        self._amount = amount

    @property
    def receipt(self):
        """Gets the receipt of this BuyCreditsRequest.  # noqa: E501


        :return: The receipt of this BuyCreditsRequest.  # noqa: E501
        :rtype: str
        """
        return self._receipt

    @receipt.setter
    def receipt(self, receipt):
        """Sets the receipt of this BuyCreditsRequest.


        :param receipt: The receipt of this BuyCreditsRequest.  # noqa: E501
        :type: str
        """

        self._receipt = receipt

    @property
    def product_id(self):
        """Gets the product_id of this BuyCreditsRequest.  # noqa: E501


        :return: The product_id of this BuyCreditsRequest.  # noqa: E501
        :rtype: int
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        """Sets the product_id of this BuyCreditsRequest.


        :param product_id: The product_id of this BuyCreditsRequest.  # noqa: E501
        :type: int
        """

        self._product_id = product_id

    @property
    def device_type(self):
        """Gets the device_type of this BuyCreditsRequest.  # noqa: E501


        :return: The device_type of this BuyCreditsRequest.  # noqa: E501
        :rtype: DeviceType
        """
        return self._device_type

    @device_type.setter
    def device_type(self, device_type):
        """Sets the device_type of this BuyCreditsRequest.


        :param device_type: The device_type of this BuyCreditsRequest.  # noqa: E501
        :type: DeviceType
        """

        self._device_type = device_type

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
        if issubclass(BuyCreditsRequest, dict):
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
        if not isinstance(other, BuyCreditsRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
