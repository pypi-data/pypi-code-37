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


class CatalogItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None, abbreviation=None, label_color=None, available_online=None, available_for_pickup=None, available_electronically=None, category_id=None, tax_ids=None, modifier_list_info=None, image_url=None, variations=None, product_type=None, skip_modifier_screen=None):
        """
        CatalogItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'description': 'str',
            'abbreviation': 'str',
            'label_color': 'str',
            'available_online': 'bool',
            'available_for_pickup': 'bool',
            'available_electronically': 'bool',
            'category_id': 'str',
            'tax_ids': 'list[str]',
            'modifier_list_info': 'list[CatalogItemModifierListInfo]',
            'image_url': 'str',
            'variations': 'list[CatalogObject]',
            'product_type': 'str',
            'skip_modifier_screen': 'bool'
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'abbreviation': 'abbreviation',
            'label_color': 'label_color',
            'available_online': 'available_online',
            'available_for_pickup': 'available_for_pickup',
            'available_electronically': 'available_electronically',
            'category_id': 'category_id',
            'tax_ids': 'tax_ids',
            'modifier_list_info': 'modifier_list_info',
            'image_url': 'image_url',
            'variations': 'variations',
            'product_type': 'product_type',
            'skip_modifier_screen': 'skip_modifier_screen'
        }

        self._name = name
        self._description = description
        self._abbreviation = abbreviation
        self._label_color = label_color
        self._available_online = available_online
        self._available_for_pickup = available_for_pickup
        self._available_electronically = available_electronically
        self._category_id = category_id
        self._tax_ids = tax_ids
        self._modifier_list_info = modifier_list_info
        self._image_url = image_url
        self._variations = variations
        self._product_type = product_type
        self._skip_modifier_screen = skip_modifier_screen

    @property
    def name(self):
        """
        Gets the name of this CatalogItem.
        The item's name. Searchable. This field must not be empty. This field has max length of 512 Unicode code points.

        :return: The name of this CatalogItem.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CatalogItem.
        The item's name. Searchable. This field must not be empty. This field has max length of 512 Unicode code points.

        :param name: The name of this CatalogItem.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this CatalogItem.
        The item's description. Searchable. This field has max length of 4096 Unicode code points.

        :return: The description of this CatalogItem.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CatalogItem.
        The item's description. Searchable. This field has max length of 4096 Unicode code points.

        :param description: The description of this CatalogItem.
        :type: str
        """

        self._description = description

    @property
    def abbreviation(self):
        """
        Gets the abbreviation of this CatalogItem.
        The text of the item's display label in the Square Point of Sale app. Only up to the first five characters of the string are used. Searchable. This field has max length of 24 Unicode code points.

        :return: The abbreviation of this CatalogItem.
        :rtype: str
        """
        return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation):
        """
        Sets the abbreviation of this CatalogItem.
        The text of the item's display label in the Square Point of Sale app. Only up to the first five characters of the string are used. Searchable. This field has max length of 24 Unicode code points.

        :param abbreviation: The abbreviation of this CatalogItem.
        :type: str
        """

        self._abbreviation = abbreviation

    @property
    def label_color(self):
        """
        Gets the label_color of this CatalogItem.
        The color of the item's display label in the Square Point of Sale app. This must be a valid hex color code.

        :return: The label_color of this CatalogItem.
        :rtype: str
        """
        return self._label_color

    @label_color.setter
    def label_color(self, label_color):
        """
        Sets the label_color of this CatalogItem.
        The color of the item's display label in the Square Point of Sale app. This must be a valid hex color code.

        :param label_color: The label_color of this CatalogItem.
        :type: str
        """

        self._label_color = label_color

    @property
    def available_online(self):
        """
        Gets the available_online of this CatalogItem.
        If `true`, the item can be added to shipping orders from the merchant's online store.

        :return: The available_online of this CatalogItem.
        :rtype: bool
        """
        return self._available_online

    @available_online.setter
    def available_online(self, available_online):
        """
        Sets the available_online of this CatalogItem.
        If `true`, the item can be added to shipping orders from the merchant's online store.

        :param available_online: The available_online of this CatalogItem.
        :type: bool
        """

        self._available_online = available_online

    @property
    def available_for_pickup(self):
        """
        Gets the available_for_pickup of this CatalogItem.
        If `true`, the item can be added to pickup orders from the merchant's online store.

        :return: The available_for_pickup of this CatalogItem.
        :rtype: bool
        """
        return self._available_for_pickup

    @available_for_pickup.setter
    def available_for_pickup(self, available_for_pickup):
        """
        Sets the available_for_pickup of this CatalogItem.
        If `true`, the item can be added to pickup orders from the merchant's online store.

        :param available_for_pickup: The available_for_pickup of this CatalogItem.
        :type: bool
        """

        self._available_for_pickup = available_for_pickup

    @property
    def available_electronically(self):
        """
        Gets the available_electronically of this CatalogItem.
        If `true`, the item can be added to electronically fulfilled orders from the merchant's online store.

        :return: The available_electronically of this CatalogItem.
        :rtype: bool
        """
        return self._available_electronically

    @available_electronically.setter
    def available_electronically(self, available_electronically):
        """
        Sets the available_electronically of this CatalogItem.
        If `true`, the item can be added to electronically fulfilled orders from the merchant's online store.

        :param available_electronically: The available_electronically of this CatalogItem.
        :type: bool
        """

        self._available_electronically = available_electronically

    @property
    def category_id(self):
        """
        Gets the category_id of this CatalogItem.
        The ID of the item's category, if any.

        :return: The category_id of this CatalogItem.
        :rtype: str
        """
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        """
        Sets the category_id of this CatalogItem.
        The ID of the item's category, if any.

        :param category_id: The category_id of this CatalogItem.
        :type: str
        """

        self._category_id = category_id

    @property
    def tax_ids(self):
        """
        Gets the tax_ids of this CatalogItem.
        A set of IDs indicating the [CatalogTax](#type-catalogtax)es that are enabled for this item. When updating an item, any taxes listed here will be added to the item. [CatalogTax](#type-catalogtax)es may also be added to or deleted from an item using `UpdateItemTaxes`.

        :return: The tax_ids of this CatalogItem.
        :rtype: list[str]
        """
        return self._tax_ids

    @tax_ids.setter
    def tax_ids(self, tax_ids):
        """
        Sets the tax_ids of this CatalogItem.
        A set of IDs indicating the [CatalogTax](#type-catalogtax)es that are enabled for this item. When updating an item, any taxes listed here will be added to the item. [CatalogTax](#type-catalogtax)es may also be added to or deleted from an item using `UpdateItemTaxes`.

        :param tax_ids: The tax_ids of this CatalogItem.
        :type: list[str]
        """

        self._tax_ids = tax_ids

    @property
    def modifier_list_info(self):
        """
        Gets the modifier_list_info of this CatalogItem.
        A set of [CatalogItemModifierListInfo](#type-catalogitemmodifierlistinfo) objects representing the modifier lists that apply to this item, along with the overrides and min and max limits that are specific to this item. [CatalogModifierList](#type-catalogmodifierlist)s may also be added to or deleted from an item using `UpdateItemModifierLists`.

        :return: The modifier_list_info of this CatalogItem.
        :rtype: list[CatalogItemModifierListInfo]
        """
        return self._modifier_list_info

    @modifier_list_info.setter
    def modifier_list_info(self, modifier_list_info):
        """
        Sets the modifier_list_info of this CatalogItem.
        A set of [CatalogItemModifierListInfo](#type-catalogitemmodifierlistinfo) objects representing the modifier lists that apply to this item, along with the overrides and min and max limits that are specific to this item. [CatalogModifierList](#type-catalogmodifierlist)s may also be added to or deleted from an item using `UpdateItemModifierLists`.

        :param modifier_list_info: The modifier_list_info of this CatalogItem.
        :type: list[CatalogItemModifierListInfo]
        """

        self._modifier_list_info = modifier_list_info

    @property
    def image_url(self):
        """
        Gets the image_url of this CatalogItem.
        __Deprecated__. The URL of an image representing this item. Deprecated in favor of `image_id` in [`CatalogObject`](#type-catalogobject).

        :return: The image_url of this CatalogItem.
        :rtype: str
        """
        return self._image_url

    @image_url.setter
    def image_url(self, image_url):
        """
        Sets the image_url of this CatalogItem.
        __Deprecated__. The URL of an image representing this item. Deprecated in favor of `image_id` in [`CatalogObject`](#type-catalogobject).

        :param image_url: The image_url of this CatalogItem.
        :type: str
        """

        self._image_url = image_url

    @property
    def variations(self):
        """
        Gets the variations of this CatalogItem.
        A list of [CatalogObject](#type-catalogobject)s containing the [CatalogItemVariation](#type-catalogitemvariation)s for this item.

        :return: The variations of this CatalogItem.
        :rtype: list[CatalogObject]
        """
        return self._variations

    @variations.setter
    def variations(self, variations):
        """
        Sets the variations of this CatalogItem.
        A list of [CatalogObject](#type-catalogobject)s containing the [CatalogItemVariation](#type-catalogitemvariation)s for this item.

        :param variations: The variations of this CatalogItem.
        :type: list[CatalogObject]
        """

        self._variations = variations

    @property
    def product_type(self):
        """
        Gets the product_type of this CatalogItem.
        The product type of the item. May not be changed once an item has been created.  Only items of product type `REGULAR` may be created by this API; items with other product types are read-only. See [CatalogItemProductType](#type-catalogitemproducttype) for possible values

        :return: The product_type of this CatalogItem.
        :rtype: str
        """
        return self._product_type

    @product_type.setter
    def product_type(self, product_type):
        """
        Sets the product_type of this CatalogItem.
        The product type of the item. May not be changed once an item has been created.  Only items of product type `REGULAR` may be created by this API; items with other product types are read-only. See [CatalogItemProductType](#type-catalogitemproducttype) for possible values

        :param product_type: The product_type of this CatalogItem.
        :type: str
        """

        self._product_type = product_type

    @property
    def skip_modifier_screen(self):
        """
        Gets the skip_modifier_screen of this CatalogItem.
        If `false`, the Square Point of Sale app will present the [CatalogItem](#type-catalogitem)'s details screen immediately, allowing the merchant to choose [CatalogModifier](#type-catalogmodifier)s before adding the item to the cart.  This is the default behavior.  If `true`, the Square Point of Sale app will immediately add the item to the cart with the pre-selected modifiers, and merchants can edit modifiers by drilling down onto the item's details.  Third-party clients are encouraged to implement similar behaviors.

        :return: The skip_modifier_screen of this CatalogItem.
        :rtype: bool
        """
        return self._skip_modifier_screen

    @skip_modifier_screen.setter
    def skip_modifier_screen(self, skip_modifier_screen):
        """
        Sets the skip_modifier_screen of this CatalogItem.
        If `false`, the Square Point of Sale app will present the [CatalogItem](#type-catalogitem)'s details screen immediately, allowing the merchant to choose [CatalogModifier](#type-catalogmodifier)s before adding the item to the cart.  This is the default behavior.  If `true`, the Square Point of Sale app will immediately add the item to the cart with the pre-selected modifiers, and merchants can edit modifiers by drilling down onto the item's details.  Third-party clients are encouraged to implement similar behaviors.

        :param skip_modifier_screen: The skip_modifier_screen of this CatalogItem.
        :type: bool
        """

        self._skip_modifier_screen = skip_modifier_screen

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
