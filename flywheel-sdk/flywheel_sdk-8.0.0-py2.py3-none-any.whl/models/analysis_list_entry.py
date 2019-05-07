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

from flywheel.models.container_parents import ContainerParents  # noqa: F401,E501
from flywheel.models.container_reference import ContainerReference  # noqa: F401,E501
from flywheel.models.file_entry import FileEntry  # noqa: F401,E501
from flywheel.models.gear_info import GearInfo  # noqa: F401,E501
from flywheel.models.note import Note  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

from .mixins import AnalysisMixin

class AnalysisListEntry(AnalysisMixin):

    swagger_types = {
        'id': 'str',
        'inputs': 'list[FileEntry]',
        'files': 'list[FileEntry]',
        'job': 'str',
        'gear_info': 'GearInfo',
        'notes': 'list[Note]',
        'description': 'str',
        'label': 'str',
        'parent': 'ContainerReference',
        'parents': 'ContainerParents',
        'created': 'datetime',
        'modified': 'datetime'
    }

    attribute_map = {
        'id': '_id',
        'inputs': 'inputs',
        'files': 'files',
        'job': 'job',
        'gear_info': 'gear_info',
        'notes': 'notes',
        'description': 'description',
        'label': 'label',
        'parent': 'parent',
        'parents': 'parents',
        'created': 'created',
        'modified': 'modified'
    }

    rattribute_map = {
        '_id': 'id',
        'inputs': 'inputs',
        'files': 'files',
        'job': 'job',
        'gear_info': 'gear_info',
        'notes': 'notes',
        'description': 'description',
        'label': 'label',
        'parent': 'parent',
        'parents': 'parents',
        'created': 'created',
        'modified': 'modified'
    }

    def __init__(self, id=None, inputs=None, files=None, job=None, gear_info=None, notes=None, description=None, label=None, parent=None, parents=None, created=None, modified=None):  # noqa: E501
        """AnalysisListEntry - a model defined in Swagger"""
        super(AnalysisListEntry, self).__init__()

        self._id = None
        self._inputs = None
        self._files = None
        self._job = None
        self._gear_info = None
        self._notes = None
        self._description = None
        self._label = None
        self._parent = None
        self._parents = None
        self._created = None
        self._modified = None
        self.discriminator = None
        self.alt_discriminator = None

        self.id = id
        if inputs is not None:
            self.inputs = inputs
        if files is not None:
            self.files = files
        if job is not None:
            self.job = job
        if gear_info is not None:
            self.gear_info = gear_info
        if notes is not None:
            self.notes = notes
        if description is not None:
            self.description = description
        self.label = label
        if parent is not None:
            self.parent = parent
        if parents is not None:
            self.parents = parents
        self.created = created
        self.modified = modified

    @property
    def id(self):
        """Gets the id of this AnalysisListEntry.

        Unique database ID

        :return: The id of this AnalysisListEntry.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AnalysisListEntry.

        Unique database ID

        :param id: The id of this AnalysisListEntry.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def inputs(self):
        """Gets the inputs of this AnalysisListEntry.


        :return: The inputs of this AnalysisListEntry.
        :rtype: list[FileEntry]
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this AnalysisListEntry.


        :param inputs: The inputs of this AnalysisListEntry.  # noqa: E501
        :type: list[FileEntry]
        """

        self._inputs = inputs

    @property
    def files(self):
        """Gets the files of this AnalysisListEntry.


        :return: The files of this AnalysisListEntry.
        :rtype: list[FileEntry]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this AnalysisListEntry.


        :param files: The files of this AnalysisListEntry.  # noqa: E501
        :type: list[FileEntry]
        """

        self._files = files

    @property
    def job(self):
        """Gets the job of this AnalysisListEntry.

        Unique database ID

        :return: The job of this AnalysisListEntry.
        :rtype: str
        """
        return self._job

    @job.setter
    def job(self, job):
        """Sets the job of this AnalysisListEntry.

        Unique database ID

        :param job: The job of this AnalysisListEntry.  # noqa: E501
        :type: str
        """

        self._job = job

    @property
    def gear_info(self):
        """Gets the gear_info of this AnalysisListEntry.


        :return: The gear_info of this AnalysisListEntry.
        :rtype: GearInfo
        """
        return self._gear_info

    @gear_info.setter
    def gear_info(self, gear_info):
        """Sets the gear_info of this AnalysisListEntry.


        :param gear_info: The gear_info of this AnalysisListEntry.  # noqa: E501
        :type: GearInfo
        """

        self._gear_info = gear_info

    @property
    def notes(self):
        """Gets the notes of this AnalysisListEntry.


        :return: The notes of this AnalysisListEntry.
        :rtype: list[Note]
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this AnalysisListEntry.


        :param notes: The notes of this AnalysisListEntry.  # noqa: E501
        :type: list[Note]
        """

        self._notes = notes

    @property
    def description(self):
        """Gets the description of this AnalysisListEntry.


        :return: The description of this AnalysisListEntry.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AnalysisListEntry.


        :param description: The description of this AnalysisListEntry.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def label(self):
        """Gets the label of this AnalysisListEntry.

        Application-specific label

        :return: The label of this AnalysisListEntry.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this AnalysisListEntry.

        Application-specific label

        :param label: The label of this AnalysisListEntry.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def parent(self):
        """Gets the parent of this AnalysisListEntry.


        :return: The parent of this AnalysisListEntry.
        :rtype: ContainerReference
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Sets the parent of this AnalysisListEntry.


        :param parent: The parent of this AnalysisListEntry.  # noqa: E501
        :type: ContainerReference
        """

        self._parent = parent

    @property
    def parents(self):
        """Gets the parents of this AnalysisListEntry.


        :return: The parents of this AnalysisListEntry.
        :rtype: ContainerParents
        """
        return self._parents

    @parents.setter
    def parents(self, parents):
        """Sets the parents of this AnalysisListEntry.


        :param parents: The parents of this AnalysisListEntry.  # noqa: E501
        :type: ContainerParents
        """

        self._parents = parents

    @property
    def created(self):
        """Gets the created of this AnalysisListEntry.

        Creation time (automatically set)

        :return: The created of this AnalysisListEntry.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this AnalysisListEntry.

        Creation time (automatically set)

        :param created: The created of this AnalysisListEntry.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this AnalysisListEntry.

        Last modification time (automatically updated)

        :return: The modified of this AnalysisListEntry.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this AnalysisListEntry.

        Last modification time (automatically updated)

        :param modified: The modified of this AnalysisListEntry.  # noqa: E501
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
        if not isinstance(other, AnalysisListEntry):
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
