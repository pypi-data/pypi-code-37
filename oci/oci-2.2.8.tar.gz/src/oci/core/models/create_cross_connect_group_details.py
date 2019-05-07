# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateCrossConnectGroupDetails(object):
    """
    CreateCrossConnectGroupDetails model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateCrossConnectGroupDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateCrossConnectGroupDetails.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateCrossConnectGroupDetails.
        :type display_name: str

        :param customer_reference_name:
            The value to assign to the customer_reference_name property of this CreateCrossConnectGroupDetails.
        :type customer_reference_name: str

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'display_name': 'str',
            'customer_reference_name': 'str'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'customer_reference_name': 'customerReferenceName'
        }

        self._compartment_id = None
        self._display_name = None
        self._customer_reference_name = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateCrossConnectGroupDetails.
        The OCID of the compartment to contain the cross-connect group.


        :return: The compartment_id of this CreateCrossConnectGroupDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateCrossConnectGroupDetails.
        The OCID of the compartment to contain the cross-connect group.


        :param compartment_id: The compartment_id of this CreateCrossConnectGroupDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateCrossConnectGroupDetails.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :return: The display_name of this CreateCrossConnectGroupDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateCrossConnectGroupDetails.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :param display_name: The display_name of this CreateCrossConnectGroupDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def customer_reference_name(self):
        """
        Gets the customer_reference_name of this CreateCrossConnectGroupDetails.
        A reference name or identifier for the physical fiber connection that this cross-connect
        group uses.


        :return: The customer_reference_name of this CreateCrossConnectGroupDetails.
        :rtype: str
        """
        return self._customer_reference_name

    @customer_reference_name.setter
    def customer_reference_name(self, customer_reference_name):
        """
        Sets the customer_reference_name of this CreateCrossConnectGroupDetails.
        A reference name or identifier for the physical fiber connection that this cross-connect
        group uses.


        :param customer_reference_name: The customer_reference_name of this CreateCrossConnectGroupDetails.
        :type: str
        """
        self._customer_reference_name = customer_reference_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
