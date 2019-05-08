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


class OrderMoneyAmounts(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, total_money=None, tax_money=None, discount_money=None, tip_money=None, service_charge_money=None):
        """
        OrderMoneyAmounts - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'total_money': 'Money',
            'tax_money': 'Money',
            'discount_money': 'Money',
            'tip_money': 'Money',
            'service_charge_money': 'Money'
        }

        self.attribute_map = {
            'total_money': 'total_money',
            'tax_money': 'tax_money',
            'discount_money': 'discount_money',
            'tip_money': 'tip_money',
            'service_charge_money': 'service_charge_money'
        }

        self._total_money = total_money
        self._tax_money = tax_money
        self._discount_money = discount_money
        self._tip_money = tip_money
        self._service_charge_money = service_charge_money

    @property
    def total_money(self):
        """
        Gets the total_money of this OrderMoneyAmounts.
        Total money.

        :return: The total_money of this OrderMoneyAmounts.
        :rtype: Money
        """
        return self._total_money

    @total_money.setter
    def total_money(self, total_money):
        """
        Sets the total_money of this OrderMoneyAmounts.
        Total money.

        :param total_money: The total_money of this OrderMoneyAmounts.
        :type: Money
        """

        self._total_money = total_money

    @property
    def tax_money(self):
        """
        Gets the tax_money of this OrderMoneyAmounts.
        Money associated with taxes.

        :return: The tax_money of this OrderMoneyAmounts.
        :rtype: Money
        """
        return self._tax_money

    @tax_money.setter
    def tax_money(self, tax_money):
        """
        Sets the tax_money of this OrderMoneyAmounts.
        Money associated with taxes.

        :param tax_money: The tax_money of this OrderMoneyAmounts.
        :type: Money
        """

        self._tax_money = tax_money

    @property
    def discount_money(self):
        """
        Gets the discount_money of this OrderMoneyAmounts.
        Money associated with discounts.

        :return: The discount_money of this OrderMoneyAmounts.
        :rtype: Money
        """
        return self._discount_money

    @discount_money.setter
    def discount_money(self, discount_money):
        """
        Sets the discount_money of this OrderMoneyAmounts.
        Money associated with discounts.

        :param discount_money: The discount_money of this OrderMoneyAmounts.
        :type: Money
        """

        self._discount_money = discount_money

    @property
    def tip_money(self):
        """
        Gets the tip_money of this OrderMoneyAmounts.
        Money associated with tips.

        :return: The tip_money of this OrderMoneyAmounts.
        :rtype: Money
        """
        return self._tip_money

    @tip_money.setter
    def tip_money(self, tip_money):
        """
        Sets the tip_money of this OrderMoneyAmounts.
        Money associated with tips.

        :param tip_money: The tip_money of this OrderMoneyAmounts.
        :type: Money
        """

        self._tip_money = tip_money

    @property
    def service_charge_money(self):
        """
        Gets the service_charge_money of this OrderMoneyAmounts.
        Money associated with service charges.

        :return: The service_charge_money of this OrderMoneyAmounts.
        :rtype: Money
        """
        return self._service_charge_money

    @service_charge_money.setter
    def service_charge_money(self, service_charge_money):
        """
        Sets the service_charge_money of this OrderMoneyAmounts.
        Money associated with service charges.

        :param service_charge_money: The service_charge_money of this OrderMoneyAmounts.
        :type: Money
        """

        self._service_charge_money = service_charge_money

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
