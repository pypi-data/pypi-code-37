# coding: utf-8

"""
Copyright 2017 Square, Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


from pprint import pformat
from six import iteritems
import re


class CreateOrderRequestLineItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, quantity=None, base_price_money=None, variation_name=None, note=None, catalog_object_id=None, modifiers=None, taxes=None, discounts=None):
        """
        CreateOrderRequestLineItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'quantity': 'str',
            'base_price_money': 'Money',
            'variation_name': 'str',
            'note': 'str',
            'catalog_object_id': 'str',
            'modifiers': 'list[CreateOrderRequestModifier]',
            'taxes': 'list[CreateOrderRequestTax]',
            'discounts': 'list[CreateOrderRequestDiscount]'
        }

        self.attribute_map = {
            'name': 'name',
            'quantity': 'quantity',
            'base_price_money': 'base_price_money',
            'variation_name': 'variation_name',
            'note': 'note',
            'catalog_object_id': 'catalog_object_id',
            'modifiers': 'modifiers',
            'taxes': 'taxes',
            'discounts': 'discounts'
        }

        self._name = name
        self._quantity = quantity
        self._base_price_money = base_price_money
        self._variation_name = variation_name
        self._note = note
        self._catalog_object_id = catalog_object_id
        self._modifiers = modifiers
        self._taxes = taxes
        self._discounts = discounts

    @property
    def name(self):
        """
        Gets the name of this CreateOrderRequestLineItem.
        Only used for ad hoc line items. The name of the line item. This value cannot exceed 500 characters.  Do not provide a value for this field if you provide a value for `catalog_object_id`.

        :return: The name of this CreateOrderRequestLineItem.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CreateOrderRequestLineItem.
        Only used for ad hoc line items. The name of the line item. This value cannot exceed 500 characters.  Do not provide a value for this field if you provide a value for `catalog_object_id`.

        :param name: The name of this CreateOrderRequestLineItem.
        :type: str
        """

        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        if len(name) > 500:
            raise ValueError("Invalid value for `name`, length must be less than `500`")

        self._name = name

    @property
    def quantity(self):
        """
        Gets the quantity of this CreateOrderRequestLineItem.
        The quantity to purchase, as a string representation of a number.  This string must have a positive integer value.

        :return: The quantity of this CreateOrderRequestLineItem.
        :rtype: str
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """
        Sets the quantity of this CreateOrderRequestLineItem.
        The quantity to purchase, as a string representation of a number.  This string must have a positive integer value.

        :param quantity: The quantity of this CreateOrderRequestLineItem.
        :type: str
        """

        if quantity is None:
            raise ValueError("Invalid value for `quantity`, must not be `None`")
        if len(quantity) > 5:
            raise ValueError("Invalid value for `quantity`, length must be less than `5`")
        if len(quantity) < 1:
            raise ValueError("Invalid value for `quantity`, length must be greater than or equal to `1`")

        self._quantity = quantity

    @property
    def base_price_money(self):
        """
        Gets the base_price_money of this CreateOrderRequestLineItem.
        The base price for a single unit of the line item.  `base_price_money` is required for ad hoc line items and variable priced [CatalogItemVariation](#type-catalogitemvariation)s. If both `catalog_object_id` and `base_price_money` are set, `base_price_money` will override the CatalogItemVariation's price.

        :return: The base_price_money of this CreateOrderRequestLineItem.
        :rtype: Money
        """
        return self._base_price_money

    @base_price_money.setter
    def base_price_money(self, base_price_money):
        """
        Sets the base_price_money of this CreateOrderRequestLineItem.
        The base price for a single unit of the line item.  `base_price_money` is required for ad hoc line items and variable priced [CatalogItemVariation](#type-catalogitemvariation)s. If both `catalog_object_id` and `base_price_money` are set, `base_price_money` will override the CatalogItemVariation's price.

        :param base_price_money: The base_price_money of this CreateOrderRequestLineItem.
        :type: Money
        """

        self._base_price_money = base_price_money

    @property
    def variation_name(self):
        """
        Gets the variation_name of this CreateOrderRequestLineItem.
        Only used for ad hoc line items. The variation name of the line item. This value cannot exceed 255 characters.  If this value is not set for an ad hoc line item, the default value of `Regular` is used.  Do not provide a value for this field if you provide a value for the `catalog_object_id`.

        :return: The variation_name of this CreateOrderRequestLineItem.
        :rtype: str
        """
        return self._variation_name

    @variation_name.setter
    def variation_name(self, variation_name):
        """
        Sets the variation_name of this CreateOrderRequestLineItem.
        Only used for ad hoc line items. The variation name of the line item. This value cannot exceed 255 characters.  If this value is not set for an ad hoc line item, the default value of `Regular` is used.  Do not provide a value for this field if you provide a value for the `catalog_object_id`.

        :param variation_name: The variation_name of this CreateOrderRequestLineItem.
        :type: str
        """

        if variation_name is None:
            raise ValueError("Invalid value for `variation_name`, must not be `None`")
        if len(variation_name) > 255:
            raise ValueError("Invalid value for `variation_name`, length must be less than `255`")

        self._variation_name = variation_name

    @property
    def note(self):
        """
        Gets the note of this CreateOrderRequestLineItem.
        The note of the line item. This value cannot exceed 500 characters.

        :return: The note of this CreateOrderRequestLineItem.
        :rtype: str
        """
        return self._note

    @note.setter
    def note(self, note):
        """
        Sets the note of this CreateOrderRequestLineItem.
        The note of the line item. This value cannot exceed 500 characters.

        :param note: The note of this CreateOrderRequestLineItem.
        :type: str
        """

        if note is None:
            raise ValueError("Invalid value for `note`, must not be `None`")
        if len(note) > 500:
            raise ValueError("Invalid value for `note`, length must be less than `500`")

        self._note = note

    @property
    def catalog_object_id(self):
        """
        Gets the catalog_object_id of this CreateOrderRequestLineItem.
        Only used for Catalog line items. The catalog object ID for an existing [CatalogItemVariation](#type-catalogitemvariation).  Do not provide a value for this field if you provide a value for `name` and `base_price_money`.

        :return: The catalog_object_id of this CreateOrderRequestLineItem.
        :rtype: str
        """
        return self._catalog_object_id

    @catalog_object_id.setter
    def catalog_object_id(self, catalog_object_id):
        """
        Sets the catalog_object_id of this CreateOrderRequestLineItem.
        Only used for Catalog line items. The catalog object ID for an existing [CatalogItemVariation](#type-catalogitemvariation).  Do not provide a value for this field if you provide a value for `name` and `base_price_money`.

        :param catalog_object_id: The catalog_object_id of this CreateOrderRequestLineItem.
        :type: str
        """

        if catalog_object_id is None:
            raise ValueError("Invalid value for `catalog_object_id`, must not be `None`")
        if len(catalog_object_id) > 192:
            raise ValueError("Invalid value for `catalog_object_id`, length must be less than `192`")

        self._catalog_object_id = catalog_object_id

    @property
    def modifiers(self):
        """
        Gets the modifiers of this CreateOrderRequestLineItem.
        Only used for Catalog line items. The modifiers to include on the line item.

        :return: The modifiers of this CreateOrderRequestLineItem.
        :rtype: list[CreateOrderRequestModifier]
        """
        return self._modifiers

    @modifiers.setter
    def modifiers(self, modifiers):
        """
        Sets the modifiers of this CreateOrderRequestLineItem.
        Only used for Catalog line items. The modifiers to include on the line item.

        :param modifiers: The modifiers of this CreateOrderRequestLineItem.
        :type: list[CreateOrderRequestModifier]
        """

        self._modifiers = modifiers

    @property
    def taxes(self):
        """
        Gets the taxes of this CreateOrderRequestLineItem.
        The taxes to include on the line item.

        :return: The taxes of this CreateOrderRequestLineItem.
        :rtype: list[CreateOrderRequestTax]
        """
        return self._taxes

    @taxes.setter
    def taxes(self, taxes):
        """
        Sets the taxes of this CreateOrderRequestLineItem.
        The taxes to include on the line item.

        :param taxes: The taxes of this CreateOrderRequestLineItem.
        :type: list[CreateOrderRequestTax]
        """

        self._taxes = taxes

    @property
    def discounts(self):
        """
        Gets the discounts of this CreateOrderRequestLineItem.
        The discounts to include on the line item.

        :return: The discounts of this CreateOrderRequestLineItem.
        :rtype: list[CreateOrderRequestDiscount]
        """
        return self._discounts

    @discounts.setter
    def discounts(self, discounts):
        """
        Sets the discounts of this CreateOrderRequestLineItem.
        The discounts to include on the line item.

        :param discounts: The discounts of this CreateOrderRequestLineItem.
        :type: list[CreateOrderRequestDiscount]
        """

        self._discounts = discounts

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
