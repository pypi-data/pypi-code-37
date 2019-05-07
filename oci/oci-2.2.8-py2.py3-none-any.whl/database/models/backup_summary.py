# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class BackupSummary(object):
    """
    A database backup.
    To use any of the API operations, you must be authorized in an IAM policy. If you're not authorized, talk to an administrator. If you're an administrator who needs to write policies to give users access, see `Getting Started with Policies`__.

    **Warning:** Oracle recommends that you avoid using any confidential information when you supply string values using the API.

    __ https://docs.cloud.oracle.com/Content/Identity/Concepts/policygetstarted.htm
    """

    #: A constant which can be used with the type property of a BackupSummary.
    #: This constant has a value of "INCREMENTAL"
    TYPE_INCREMENTAL = "INCREMENTAL"

    #: A constant which can be used with the type property of a BackupSummary.
    #: This constant has a value of "FULL"
    TYPE_FULL = "FULL"

    #: A constant which can be used with the lifecycle_state property of a BackupSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a BackupSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a BackupSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a BackupSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a BackupSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a BackupSummary.
    #: This constant has a value of "RESTORING"
    LIFECYCLE_STATE_RESTORING = "RESTORING"

    #: A constant which can be used with the database_edition property of a BackupSummary.
    #: This constant has a value of "STANDARD_EDITION"
    DATABASE_EDITION_STANDARD_EDITION = "STANDARD_EDITION"

    #: A constant which can be used with the database_edition property of a BackupSummary.
    #: This constant has a value of "ENTERPRISE_EDITION"
    DATABASE_EDITION_ENTERPRISE_EDITION = "ENTERPRISE_EDITION"

    #: A constant which can be used with the database_edition property of a BackupSummary.
    #: This constant has a value of "ENTERPRISE_EDITION_HIGH_PERFORMANCE"
    DATABASE_EDITION_ENTERPRISE_EDITION_HIGH_PERFORMANCE = "ENTERPRISE_EDITION_HIGH_PERFORMANCE"

    #: A constant which can be used with the database_edition property of a BackupSummary.
    #: This constant has a value of "ENTERPRISE_EDITION_EXTREME_PERFORMANCE"
    DATABASE_EDITION_ENTERPRISE_EDITION_EXTREME_PERFORMANCE = "ENTERPRISE_EDITION_EXTREME_PERFORMANCE"

    def __init__(self, **kwargs):
        """
        Initializes a new BackupSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this BackupSummary.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this BackupSummary.
        :type compartment_id: str

        :param database_id:
            The value to assign to the database_id property of this BackupSummary.
        :type database_id: str

        :param display_name:
            The value to assign to the display_name property of this BackupSummary.
        :type display_name: str

        :param type:
            The value to assign to the type property of this BackupSummary.
            Allowed values for this property are: "INCREMENTAL", "FULL", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param time_started:
            The value to assign to the time_started property of this BackupSummary.
        :type time_started: datetime

        :param time_ended:
            The value to assign to the time_ended property of this BackupSummary.
        :type time_ended: datetime

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this BackupSummary.
        :type lifecycle_details: str

        :param availability_domain:
            The value to assign to the availability_domain property of this BackupSummary.
        :type availability_domain: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this BackupSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "DELETING", "DELETED", "FAILED", "RESTORING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param database_edition:
            The value to assign to the database_edition property of this BackupSummary.
            Allowed values for this property are: "STANDARD_EDITION", "ENTERPRISE_EDITION", "ENTERPRISE_EDITION_HIGH_PERFORMANCE", "ENTERPRISE_EDITION_EXTREME_PERFORMANCE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type database_edition: str

        :param database_size_in_gbs:
            The value to assign to the database_size_in_gbs property of this BackupSummary.
        :type database_size_in_gbs: float

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'database_id': 'str',
            'display_name': 'str',
            'type': 'str',
            'time_started': 'datetime',
            'time_ended': 'datetime',
            'lifecycle_details': 'str',
            'availability_domain': 'str',
            'lifecycle_state': 'str',
            'database_edition': 'str',
            'database_size_in_gbs': 'float'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'database_id': 'databaseId',
            'display_name': 'displayName',
            'type': 'type',
            'time_started': 'timeStarted',
            'time_ended': 'timeEnded',
            'lifecycle_details': 'lifecycleDetails',
            'availability_domain': 'availabilityDomain',
            'lifecycle_state': 'lifecycleState',
            'database_edition': 'databaseEdition',
            'database_size_in_gbs': 'databaseSizeInGBs'
        }

        self._id = None
        self._compartment_id = None
        self._database_id = None
        self._display_name = None
        self._type = None
        self._time_started = None
        self._time_ended = None
        self._lifecycle_details = None
        self._availability_domain = None
        self._lifecycle_state = None
        self._database_edition = None
        self._database_size_in_gbs = None

    @property
    def id(self):
        """
        Gets the id of this BackupSummary.
        The `OCID`__ of the backup.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this BackupSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this BackupSummary.
        The `OCID`__ of the backup.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this BackupSummary.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this BackupSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this BackupSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this BackupSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this BackupSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def database_id(self):
        """
        Gets the database_id of this BackupSummary.
        The `OCID`__ of the database.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The database_id of this BackupSummary.
        :rtype: str
        """
        return self._database_id

    @database_id.setter
    def database_id(self, database_id):
        """
        Sets the database_id of this BackupSummary.
        The `OCID`__ of the database.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param database_id: The database_id of this BackupSummary.
        :type: str
        """
        self._database_id = database_id

    @property
    def display_name(self):
        """
        Gets the display_name of this BackupSummary.
        The user-friendly name for the backup. The name does not have to be unique.


        :return: The display_name of this BackupSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this BackupSummary.
        The user-friendly name for the backup. The name does not have to be unique.


        :param display_name: The display_name of this BackupSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def type(self):
        """
        Gets the type of this BackupSummary.
        The type of backup.

        Allowed values for this property are: "INCREMENTAL", "FULL", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this BackupSummary.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this BackupSummary.
        The type of backup.


        :param type: The type of this BackupSummary.
        :type: str
        """
        allowed_values = ["INCREMENTAL", "FULL"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def time_started(self):
        """
        Gets the time_started of this BackupSummary.
        The date and time the backup started.


        :return: The time_started of this BackupSummary.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this BackupSummary.
        The date and time the backup started.


        :param time_started: The time_started of this BackupSummary.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_ended(self):
        """
        Gets the time_ended of this BackupSummary.
        The date and time the backup was completed.


        :return: The time_ended of this BackupSummary.
        :rtype: datetime
        """
        return self._time_ended

    @time_ended.setter
    def time_ended(self, time_ended):
        """
        Sets the time_ended of this BackupSummary.
        The date and time the backup was completed.


        :param time_ended: The time_ended of this BackupSummary.
        :type: datetime
        """
        self._time_ended = time_ended

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this BackupSummary.
        Additional information about the current lifecycleState.


        :return: The lifecycle_details of this BackupSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this BackupSummary.
        Additional information about the current lifecycleState.


        :param lifecycle_details: The lifecycle_details of this BackupSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def availability_domain(self):
        """
        Gets the availability_domain of this BackupSummary.
        The name of the availability domain where the database backup is stored.


        :return: The availability_domain of this BackupSummary.
        :rtype: str
        """
        return self._availability_domain

    @availability_domain.setter
    def availability_domain(self, availability_domain):
        """
        Sets the availability_domain of this BackupSummary.
        The name of the availability domain where the database backup is stored.


        :param availability_domain: The availability_domain of this BackupSummary.
        :type: str
        """
        self._availability_domain = availability_domain

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this BackupSummary.
        The current state of the backup.

        Allowed values for this property are: "CREATING", "ACTIVE", "DELETING", "DELETED", "FAILED", "RESTORING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this BackupSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this BackupSummary.
        The current state of the backup.


        :param lifecycle_state: The lifecycle_state of this BackupSummary.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "DELETING", "DELETED", "FAILED", "RESTORING"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def database_edition(self):
        """
        Gets the database_edition of this BackupSummary.
        The Oracle Database edition of the DB system from which the database backup was taken.

        Allowed values for this property are: "STANDARD_EDITION", "ENTERPRISE_EDITION", "ENTERPRISE_EDITION_HIGH_PERFORMANCE", "ENTERPRISE_EDITION_EXTREME_PERFORMANCE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The database_edition of this BackupSummary.
        :rtype: str
        """
        return self._database_edition

    @database_edition.setter
    def database_edition(self, database_edition):
        """
        Sets the database_edition of this BackupSummary.
        The Oracle Database edition of the DB system from which the database backup was taken.


        :param database_edition: The database_edition of this BackupSummary.
        :type: str
        """
        allowed_values = ["STANDARD_EDITION", "ENTERPRISE_EDITION", "ENTERPRISE_EDITION_HIGH_PERFORMANCE", "ENTERPRISE_EDITION_EXTREME_PERFORMANCE"]
        if not value_allowed_none_or_none_sentinel(database_edition, allowed_values):
            database_edition = 'UNKNOWN_ENUM_VALUE'
        self._database_edition = database_edition

    @property
    def database_size_in_gbs(self):
        """
        Gets the database_size_in_gbs of this BackupSummary.
        The size of the database in gigabytes at the time the backup was taken.


        :return: The database_size_in_gbs of this BackupSummary.
        :rtype: float
        """
        return self._database_size_in_gbs

    @database_size_in_gbs.setter
    def database_size_in_gbs(self, database_size_in_gbs):
        """
        Sets the database_size_in_gbs of this BackupSummary.
        The size of the database in gigabytes at the time the backup was taken.


        :param database_size_in_gbs: The database_size_in_gbs of this BackupSummary.
        :type: float
        """
        self._database_size_in_gbs = database_size_in_gbs

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
