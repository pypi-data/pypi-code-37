# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 8.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

from flywheel.models.file_entry import FileEntry  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class ContainerOutputWithFiles(object):

    swagger_types = {
        'id': 'str',
        'label': 'str',
        'files': 'list[FileEntry]',
        'created': 'datetime',
        'modified': 'datetime'
    }

    attribute_map = {
        'id': '_id',
        'label': 'label',
        'files': 'files',
        'created': 'created',
        'modified': 'modified'
    }

    rattribute_map = {
        '_id': 'id',
        'label': 'label',
        'files': 'files',
        'created': 'created',
        'modified': 'modified'
    }

    def __init__(self, id=None, label=None, files=None, created=None, modified=None):  # noqa: E501
        """ContainerOutputWithFiles - a model defined in Swagger"""
        super(ContainerOutputWithFiles, self).__init__()

        self._id = None
        self._label = None
        self._files = None
        self._created = None
        self._modified = None
        self.discriminator = None
        self.alt_discriminator = None

        if id is not None:
            self.id = id
        if label is not None:
            self.label = label
        if files is not None:
            self.files = files
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified

    @property
    def id(self):
        """Gets the id of this ContainerOutputWithFiles.

        Unique database ID

        :return: The id of this ContainerOutputWithFiles.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ContainerOutputWithFiles.

        Unique database ID

        :param id: The id of this ContainerOutputWithFiles.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def label(self):
        """Gets the label of this ContainerOutputWithFiles.

        Application-specific label

        :return: The label of this ContainerOutputWithFiles.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this ContainerOutputWithFiles.

        Application-specific label

        :param label: The label of this ContainerOutputWithFiles.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def files(self):
        """Gets the files of this ContainerOutputWithFiles.


        :return: The files of this ContainerOutputWithFiles.
        :rtype: list[FileEntry]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this ContainerOutputWithFiles.


        :param files: The files of this ContainerOutputWithFiles.  # noqa: E501
        :type: list[FileEntry]
        """

        self._files = files

    @property
    def created(self):
        """Gets the created of this ContainerOutputWithFiles.

        Creation time (automatically set)

        :return: The created of this ContainerOutputWithFiles.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this ContainerOutputWithFiles.

        Creation time (automatically set)

        :param created: The created of this ContainerOutputWithFiles.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this ContainerOutputWithFiles.

        Last modification time (automatically updated)

        :return: The modified of this ContainerOutputWithFiles.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this ContainerOutputWithFiles.

        Last modification time (automatically updated)

        :param modified: The modified of this ContainerOutputWithFiles.  # noqa: E501
        :type: datetime
        """

        self._modified = modified


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ContainerOutputWithFiles):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result
