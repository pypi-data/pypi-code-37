# coding: utf-8

"""
    Aspose.PDF Cloud API Reference


   Copyright (c) 2019 Aspose.PDF Cloud
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.



    OpenAPI spec version: 2.0
    
"""


from pprint import pformat
from six import iteritems
import re


class RowRecognized(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
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
        'cell_list': 'list[CellRecognized]',
        'rectangle': 'Rectangle'
    }

    attribute_map = {
        'cell_list': 'CellList',
        'rectangle': 'Rectangle'
    }

    def __init__(self, cell_list=None, rectangle=None):
        """
        RowRecognized - a model defined in Swagger
        """

        self._cell_list = None
        self._rectangle = None

        if cell_list is not None:
          self.cell_list = cell_list
        if rectangle is not None:
          self.rectangle = rectangle

    @property
    def cell_list(self):
        """
        Gets the cell_list of this RowRecognized.
        Gets readonly IList containing cells of the row

        :return: The cell_list of this RowRecognized.
        :rtype: list[CellRecognized]
        """
        return self._cell_list

    @cell_list.setter
    def cell_list(self, cell_list):
        """
        Sets the cell_list of this RowRecognized.
        Gets readonly IList containing cells of the row

        :param cell_list: The cell_list of this RowRecognized.
        :type: list[CellRecognized]
        """

        self._cell_list = cell_list

    @property
    def rectangle(self):
        """
        Gets the rectangle of this RowRecognized.
        Gets rectangle that describes position of the row on page

        :return: The rectangle of this RowRecognized.
        :rtype: Rectangle
        """
        return self._rectangle

    @rectangle.setter
    def rectangle(self, rectangle):
        """
        Sets the rectangle of this RowRecognized.
        Gets rectangle that describes position of the row on page

        :param rectangle: The rectangle of this RowRecognized.
        :type: Rectangle
        """

        self._rectangle = rectangle

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
        if not isinstance(other, RowRecognized):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
