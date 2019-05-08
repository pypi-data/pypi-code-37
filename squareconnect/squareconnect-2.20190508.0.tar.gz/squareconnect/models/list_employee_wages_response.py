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


class ListEmployeeWagesResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, employee_wages=None, cursor=None, errors=None):
        """
        ListEmployeeWagesResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'employee_wages': 'list[EmployeeWage]',
            'cursor': 'str',
            'errors': 'list[Error]'
        }

        self.attribute_map = {
            'employee_wages': 'employee_wages',
            'cursor': 'cursor',
            'errors': 'errors'
        }

        self._employee_wages = employee_wages
        self._cursor = cursor
        self._errors = errors

    @property
    def employee_wages(self):
        """
        Gets the employee_wages of this ListEmployeeWagesResponse.
        A page of Employee Wage results.

        :return: The employee_wages of this ListEmployeeWagesResponse.
        :rtype: list[EmployeeWage]
        """
        return self._employee_wages

    @employee_wages.setter
    def employee_wages(self, employee_wages):
        """
        Sets the employee_wages of this ListEmployeeWagesResponse.
        A page of Employee Wage results.

        :param employee_wages: The employee_wages of this ListEmployeeWagesResponse.
        :type: list[EmployeeWage]
        """

        self._employee_wages = employee_wages

    @property
    def cursor(self):
        """
        Gets the cursor of this ListEmployeeWagesResponse.
        Value supplied in the subsequent request to fetch the next next page of Employee Wage results.

        :return: The cursor of this ListEmployeeWagesResponse.
        :rtype: str
        """
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        """
        Sets the cursor of this ListEmployeeWagesResponse.
        Value supplied in the subsequent request to fetch the next next page of Employee Wage results.

        :param cursor: The cursor of this ListEmployeeWagesResponse.
        :type: str
        """

        self._cursor = cursor

    @property
    def errors(self):
        """
        Gets the errors of this ListEmployeeWagesResponse.
        Any errors that occurred during the request.

        :return: The errors of this ListEmployeeWagesResponse.
        :rtype: list[Error]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """
        Sets the errors of this ListEmployeeWagesResponse.
        Any errors that occurred during the request.

        :param errors: The errors of this ListEmployeeWagesResponse.
        :type: list[Error]
        """

        self._errors = errors

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
