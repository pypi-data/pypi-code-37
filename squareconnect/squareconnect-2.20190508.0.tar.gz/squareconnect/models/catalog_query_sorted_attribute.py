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


class CatalogQuerySortedAttribute(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, attribute_name=None, initial_attribute_value=None, sort_order=None):
        """
        CatalogQuerySortedAttribute - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'attribute_name': 'str',
            'initial_attribute_value': 'str',
            'sort_order': 'str'
        }

        self.attribute_map = {
            'attribute_name': 'attribute_name',
            'initial_attribute_value': 'initial_attribute_value',
            'sort_order': 'sort_order'
        }

        self._attribute_name = attribute_name
        self._initial_attribute_value = initial_attribute_value
        self._sort_order = sort_order

    @property
    def attribute_name(self):
        """
        Gets the attribute_name of this CatalogQuerySortedAttribute.
        The attribute whose value should be used as the sort key.

        :return: The attribute_name of this CatalogQuerySortedAttribute.
        :rtype: str
        """
        return self._attribute_name

    @attribute_name.setter
    def attribute_name(self, attribute_name):
        """
        Sets the attribute_name of this CatalogQuerySortedAttribute.
        The attribute whose value should be used as the sort key.

        :param attribute_name: The attribute_name of this CatalogQuerySortedAttribute.
        :type: str
        """

        if attribute_name is None:
            raise ValueError("Invalid value for `attribute_name`, must not be `None`")
        if len(attribute_name) < 1:
            raise ValueError("Invalid value for `attribute_name`, length must be greater than or equal to `1`")

        self._attribute_name = attribute_name

    @property
    def initial_attribute_value(self):
        """
        Gets the initial_attribute_value of this CatalogQuerySortedAttribute.
        The first attribute value to be returned by the query. Ascending sorts will return only objects with this value or greater, while descending sorts will return only objects with this value or less. If unset, start at the beginning (for ascending sorts) or end (for descending sorts).

        :return: The initial_attribute_value of this CatalogQuerySortedAttribute.
        :rtype: str
        """
        return self._initial_attribute_value

    @initial_attribute_value.setter
    def initial_attribute_value(self, initial_attribute_value):
        """
        Sets the initial_attribute_value of this CatalogQuerySortedAttribute.
        The first attribute value to be returned by the query. Ascending sorts will return only objects with this value or greater, while descending sorts will return only objects with this value or less. If unset, start at the beginning (for ascending sorts) or end (for descending sorts).

        :param initial_attribute_value: The initial_attribute_value of this CatalogQuerySortedAttribute.
        :type: str
        """

        self._initial_attribute_value = initial_attribute_value

    @property
    def sort_order(self):
        """
        Gets the sort_order of this CatalogQuerySortedAttribute.
        The desired [SortOrder](#type-sortorder), `\"ASC\"` (ascending) or `\"DESC\"` (descending). See [SortOrder](#type-sortorder) for possible values

        :return: The sort_order of this CatalogQuerySortedAttribute.
        :rtype: str
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """
        Sets the sort_order of this CatalogQuerySortedAttribute.
        The desired [SortOrder](#type-sortorder), `\"ASC\"` (ascending) or `\"DESC\"` (descending). See [SortOrder](#type-sortorder) for possible values

        :param sort_order: The sort_order of this CatalogQuerySortedAttribute.
        :type: str
        """

        self._sort_order = sort_order

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
