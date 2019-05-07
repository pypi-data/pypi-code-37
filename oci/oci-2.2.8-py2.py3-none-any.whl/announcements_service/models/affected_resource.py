# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AffectedResource(object):
    """
    The resource affected by the event described in the announcement.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AffectedResource object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param resource_id:
            The value to assign to the resource_id property of this AffectedResource.
        :type resource_id: str

        :param resource_name:
            The value to assign to the resource_name property of this AffectedResource.
        :type resource_name: str

        :param region:
            The value to assign to the region property of this AffectedResource.
        :type region: str

        """
        self.swagger_types = {
            'resource_id': 'str',
            'resource_name': 'str',
            'region': 'str'
        }

        self.attribute_map = {
            'resource_id': 'resourceId',
            'resource_name': 'resourceName',
            'region': 'region'
        }

        self._resource_id = None
        self._resource_name = None
        self._region = None

    @property
    def resource_id(self):
        """
        **[Required]** Gets the resource_id of this AffectedResource.
        The OCID of the affected resource.


        :return: The resource_id of this AffectedResource.
        :rtype: str
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """
        Sets the resource_id of this AffectedResource.
        The OCID of the affected resource.


        :param resource_id: The resource_id of this AffectedResource.
        :type: str
        """
        self._resource_id = resource_id

    @property
    def resource_name(self):
        """
        **[Required]** Gets the resource_name of this AffectedResource.
        The friendly name of the resource.


        :return: The resource_name of this AffectedResource.
        :rtype: str
        """
        return self._resource_name

    @resource_name.setter
    def resource_name(self, resource_name):
        """
        Sets the resource_name of this AffectedResource.
        The friendly name of the resource.


        :param resource_name: The resource_name of this AffectedResource.
        :type: str
        """
        self._resource_name = resource_name

    @property
    def region(self):
        """
        **[Required]** Gets the region of this AffectedResource.
        The region where the affected resource exists.


        :return: The region of this AffectedResource.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """
        Sets the region of this AffectedResource.
        The region where the affected resource exists.


        :param region: The region of this AffectedResource.
        :type: str
        """
        self._region = region

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
