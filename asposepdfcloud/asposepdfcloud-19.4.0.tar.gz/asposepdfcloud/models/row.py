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


class Row(object):
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
        'background_color': 'Color',
        'border': 'BorderInfo',
        'cells': 'list[Cell]',
        'default_cell_border': 'BorderInfo',
        'min_row_height': 'float',
        'fixed_row_height': 'float',
        'is_in_new_page': 'bool',
        'is_row_broken': 'bool',
        'default_cell_text_state': 'TextState',
        'default_cell_padding': 'MarginInfo',
        'vertical_alignment': 'VerticalAlignment'
    }

    attribute_map = {
        'background_color': 'BackgroundColor',
        'border': 'Border',
        'cells': 'Cells',
        'default_cell_border': 'DefaultCellBorder',
        'min_row_height': 'MinRowHeight',
        'fixed_row_height': 'FixedRowHeight',
        'is_in_new_page': 'IsInNewPage',
        'is_row_broken': 'IsRowBroken',
        'default_cell_text_state': 'DefaultCellTextState',
        'default_cell_padding': 'DefaultCellPadding',
        'vertical_alignment': 'VerticalAlignment'
    }

    def __init__(self, background_color=None, border=None, cells=None, default_cell_border=None, min_row_height=None, fixed_row_height=None, is_in_new_page=None, is_row_broken=None, default_cell_text_state=None, default_cell_padding=None, vertical_alignment=None):
        """
        Row - a model defined in Swagger
        """

        self._background_color = None
        self._border = None
        self._cells = None
        self._default_cell_border = None
        self._min_row_height = None
        self._fixed_row_height = None
        self._is_in_new_page = None
        self._is_row_broken = None
        self._default_cell_text_state = None
        self._default_cell_padding = None
        self._vertical_alignment = None

        if background_color is not None:
          self.background_color = background_color
        if border is not None:
          self.border = border
        self.cells = cells
        if default_cell_border is not None:
          self.default_cell_border = default_cell_border
        if min_row_height is not None:
          self.min_row_height = min_row_height
        if fixed_row_height is not None:
          self.fixed_row_height = fixed_row_height
        if is_in_new_page is not None:
          self.is_in_new_page = is_in_new_page
        if is_row_broken is not None:
          self.is_row_broken = is_row_broken
        if default_cell_text_state is not None:
          self.default_cell_text_state = default_cell_text_state
        if default_cell_padding is not None:
          self.default_cell_padding = default_cell_padding
        if vertical_alignment is not None:
          self.vertical_alignment = vertical_alignment

    @property
    def background_color(self):
        """
        Gets the background_color of this Row.
        Gets or sets the background color.

        :return: The background_color of this Row.
        :rtype: Color
        """
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        """
        Sets the background_color of this Row.
        Gets or sets the background color.

        :param background_color: The background_color of this Row.
        :type: Color
        """

        self._background_color = background_color

    @property
    def border(self):
        """
        Gets the border of this Row.
        Gets or sets the border.

        :return: The border of this Row.
        :rtype: BorderInfo
        """
        return self._border

    @border.setter
    def border(self, border):
        """
        Sets the border of this Row.
        Gets or sets the border.

        :param border: The border of this Row.
        :type: BorderInfo
        """

        self._border = border

    @property
    def cells(self):
        """
        Gets the cells of this Row.
        Sets the cells of the row.

        :return: The cells of this Row.
        :rtype: list[Cell]
        """
        return self._cells

    @cells.setter
    def cells(self, cells):
        """
        Sets the cells of this Row.
        Sets the cells of the row.

        :param cells: The cells of this Row.
        :type: list[Cell]
        """
        if cells is None:
            raise ValueError("Invalid value for `cells`, must not be `None`")

        self._cells = cells

    @property
    def default_cell_border(self):
        """
        Gets the default_cell_border of this Row.
        Gets default cell border;

        :return: The default_cell_border of this Row.
        :rtype: BorderInfo
        """
        return self._default_cell_border

    @default_cell_border.setter
    def default_cell_border(self, default_cell_border):
        """
        Sets the default_cell_border of this Row.
        Gets default cell border;

        :param default_cell_border: The default_cell_border of this Row.
        :type: BorderInfo
        """

        self._default_cell_border = default_cell_border

    @property
    def min_row_height(self):
        """
        Gets the min_row_height of this Row.
        Gets height for row;

        :return: The min_row_height of this Row.
        :rtype: float
        """
        return self._min_row_height

    @min_row_height.setter
    def min_row_height(self, min_row_height):
        """
        Sets the min_row_height of this Row.
        Gets height for row;

        :param min_row_height: The min_row_height of this Row.
        :type: float
        """

        self._min_row_height = min_row_height

    @property
    def fixed_row_height(self):
        """
        Gets the fixed_row_height of this Row.
        Gets fixed row height - row may have fixed height;

        :return: The fixed_row_height of this Row.
        :rtype: float
        """
        return self._fixed_row_height

    @fixed_row_height.setter
    def fixed_row_height(self, fixed_row_height):
        """
        Sets the fixed_row_height of this Row.
        Gets fixed row height - row may have fixed height;

        :param fixed_row_height: The fixed_row_height of this Row.
        :type: float
        """

        self._fixed_row_height = fixed_row_height

    @property
    def is_in_new_page(self):
        """
        Gets the is_in_new_page of this Row.
        Gets fixed row is in new page - page with this property should be printed to next page Default false;

        :return: The is_in_new_page of this Row.
        :rtype: bool
        """
        return self._is_in_new_page

    @is_in_new_page.setter
    def is_in_new_page(self, is_in_new_page):
        """
        Sets the is_in_new_page of this Row.
        Gets fixed row is in new page - page with this property should be printed to next page Default false;

        :param is_in_new_page: The is_in_new_page of this Row.
        :type: bool
        """

        self._is_in_new_page = is_in_new_page

    @property
    def is_row_broken(self):
        """
        Gets the is_row_broken of this Row.
        Gets is row can be broken between two pages

        :return: The is_row_broken of this Row.
        :rtype: bool
        """
        return self._is_row_broken

    @is_row_broken.setter
    def is_row_broken(self, is_row_broken):
        """
        Sets the is_row_broken of this Row.
        Gets is row can be broken between two pages

        :param is_row_broken: The is_row_broken of this Row.
        :type: bool
        """

        self._is_row_broken = is_row_broken

    @property
    def default_cell_text_state(self):
        """
        Gets the default_cell_text_state of this Row.
        Gets or sets default text state for row cells

        :return: The default_cell_text_state of this Row.
        :rtype: TextState
        """
        return self._default_cell_text_state

    @default_cell_text_state.setter
    def default_cell_text_state(self, default_cell_text_state):
        """
        Sets the default_cell_text_state of this Row.
        Gets or sets default text state for row cells

        :param default_cell_text_state: The default_cell_text_state of this Row.
        :type: TextState
        """

        self._default_cell_text_state = default_cell_text_state

    @property
    def default_cell_padding(self):
        """
        Gets the default_cell_padding of this Row.
        Gets or sets default margin for row cells

        :return: The default_cell_padding of this Row.
        :rtype: MarginInfo
        """
        return self._default_cell_padding

    @default_cell_padding.setter
    def default_cell_padding(self, default_cell_padding):
        """
        Sets the default_cell_padding of this Row.
        Gets or sets default margin for row cells

        :param default_cell_padding: The default_cell_padding of this Row.
        :type: MarginInfo
        """

        self._default_cell_padding = default_cell_padding

    @property
    def vertical_alignment(self):
        """
        Gets the vertical_alignment of this Row.
        Gets or sets the vertical alignment.

        :return: The vertical_alignment of this Row.
        :rtype: VerticalAlignment
        """
        return self._vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, vertical_alignment):
        """
        Sets the vertical_alignment of this Row.
        Gets or sets the vertical alignment.

        :param vertical_alignment: The vertical_alignment of this Row.
        :type: VerticalAlignment
        """

        self._vertical_alignment = vertical_alignment

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
        if not isinstance(other, Row):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
