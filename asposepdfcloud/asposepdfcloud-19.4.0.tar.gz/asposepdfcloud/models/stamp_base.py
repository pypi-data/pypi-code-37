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


class StampBase(object):
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
        'links': 'list[Link]',
        'background': 'bool',
        'horizontal_alignment': 'HorizontalAlignment',
        'opacity': 'float',
        'rotate': 'Rotation',
        'rotate_angle': 'float',
        'x_indent': 'float',
        'y_indent': 'float',
        'zoom': 'float'
    }

    attribute_map = {
        'links': 'Links',
        'background': 'Background',
        'horizontal_alignment': 'HorizontalAlignment',
        'opacity': 'Opacity',
        'rotate': 'Rotate',
        'rotate_angle': 'RotateAngle',
        'x_indent': 'XIndent',
        'y_indent': 'YIndent',
        'zoom': 'Zoom'
    }

    def __init__(self, links=None, background=None, horizontal_alignment=None, opacity=None, rotate=None, rotate_angle=None, x_indent=None, y_indent=None, zoom=None):
        """
        StampBase - a model defined in Swagger
        """

        self._links = None
        self._background = None
        self._horizontal_alignment = None
        self._opacity = None
        self._rotate = None
        self._rotate_angle = None
        self._x_indent = None
        self._y_indent = None
        self._zoom = None

        if links is not None:
          self.links = links
        if background is not None:
          self.background = background
        if horizontal_alignment is not None:
          self.horizontal_alignment = horizontal_alignment
        if opacity is not None:
          self.opacity = opacity
        if rotate is not None:
          self.rotate = rotate
        if rotate_angle is not None:
          self.rotate_angle = rotate_angle
        if x_indent is not None:
          self.x_indent = x_indent
        if y_indent is not None:
          self.y_indent = y_indent
        if zoom is not None:
          self.zoom = zoom

    @property
    def links(self):
        """
        Gets the links of this StampBase.
        Link to the document.

        :return: The links of this StampBase.
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """
        Sets the links of this StampBase.
        Link to the document.

        :param links: The links of this StampBase.
        :type: list[Link]
        """

        self._links = links

    @property
    def background(self):
        """
        Gets the background of this StampBase.
        Sets or gets a bool value that indicates the content is stamped as background. If the value is true, the stamp content is layed at the bottom. By defalt, the value is false, the stamp content is layed at the top.

        :return: The background of this StampBase.
        :rtype: bool
        """
        return self._background

    @background.setter
    def background(self, background):
        """
        Sets the background of this StampBase.
        Sets or gets a bool value that indicates the content is stamped as background. If the value is true, the stamp content is layed at the bottom. By defalt, the value is false, the stamp content is layed at the top.

        :param background: The background of this StampBase.
        :type: bool
        """

        self._background = background

    @property
    def horizontal_alignment(self):
        """
        Gets the horizontal_alignment of this StampBase.
        Gets or sets Horizontal alignment of stamp on the page. 

        :return: The horizontal_alignment of this StampBase.
        :rtype: HorizontalAlignment
        """
        return self._horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, horizontal_alignment):
        """
        Sets the horizontal_alignment of this StampBase.
        Gets or sets Horizontal alignment of stamp on the page. 

        :param horizontal_alignment: The horizontal_alignment of this StampBase.
        :type: HorizontalAlignment
        """

        self._horizontal_alignment = horizontal_alignment

    @property
    def opacity(self):
        """
        Gets the opacity of this StampBase.
        Gets or sets a value to indicate the stamp opacity. The value is from 0.0 to 1.0. By default the value is 1.0.

        :return: The opacity of this StampBase.
        :rtype: float
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        """
        Sets the opacity of this StampBase.
        Gets or sets a value to indicate the stamp opacity. The value is from 0.0 to 1.0. By default the value is 1.0.

        :param opacity: The opacity of this StampBase.
        :type: float
        """

        self._opacity = opacity

    @property
    def rotate(self):
        """
        Gets the rotate of this StampBase.
        Sets or gets the rotation of stamp content according  values. Note. This property is for set angles which are multiples of 90 degrees (0, 90, 180, 270 degrees). To set arbitrary angle use RotateAngle property.  If angle set by ArbitraryAngle is not multiple of 90 then Rotate property returns Rotation.None.

        :return: The rotate of this StampBase.
        :rtype: Rotation
        """
        return self._rotate

    @rotate.setter
    def rotate(self, rotate):
        """
        Sets the rotate of this StampBase.
        Sets or gets the rotation of stamp content according  values. Note. This property is for set angles which are multiples of 90 degrees (0, 90, 180, 270 degrees). To set arbitrary angle use RotateAngle property.  If angle set by ArbitraryAngle is not multiple of 90 then Rotate property returns Rotation.None.

        :param rotate: The rotate of this StampBase.
        :type: Rotation
        """

        self._rotate = rotate

    @property
    def rotate_angle(self):
        """
        Gets the rotate_angle of this StampBase.
        Gets or sets rotate angle of stamp in degrees. This property allows to set arbitrary rotate angle. 

        :return: The rotate_angle of this StampBase.
        :rtype: float
        """
        return self._rotate_angle

    @rotate_angle.setter
    def rotate_angle(self, rotate_angle):
        """
        Sets the rotate_angle of this StampBase.
        Gets or sets rotate angle of stamp in degrees. This property allows to set arbitrary rotate angle. 

        :param rotate_angle: The rotate_angle of this StampBase.
        :type: float
        """

        self._rotate_angle = rotate_angle

    @property
    def x_indent(self):
        """
        Gets the x_indent of this StampBase.
        Horizontal stamp coordinate, starting from the left.

        :return: The x_indent of this StampBase.
        :rtype: float
        """
        return self._x_indent

    @x_indent.setter
    def x_indent(self, x_indent):
        """
        Sets the x_indent of this StampBase.
        Horizontal stamp coordinate, starting from the left.

        :param x_indent: The x_indent of this StampBase.
        :type: float
        """

        self._x_indent = x_indent

    @property
    def y_indent(self):
        """
        Gets the y_indent of this StampBase.
        Vertical stamp coordinate, starting from the bottom.

        :return: The y_indent of this StampBase.
        :rtype: float
        """
        return self._y_indent

    @y_indent.setter
    def y_indent(self, y_indent):
        """
        Sets the y_indent of this StampBase.
        Vertical stamp coordinate, starting from the bottom.

        :param y_indent: The y_indent of this StampBase.
        :type: float
        """

        self._y_indent = y_indent

    @property
    def zoom(self):
        """
        Gets the zoom of this StampBase.
        Zooming factor of the stamp. Allows to scale stamp.

        :return: The zoom of this StampBase.
        :rtype: float
        """
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        """
        Sets the zoom of this StampBase.
        Zooming factor of the stamp. Allows to scale stamp.

        :param zoom: The zoom of this StampBase.
        :type: float
        """

        self._zoom = zoom

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
        if not isinstance(other, StampBase):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
