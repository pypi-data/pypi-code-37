# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AggregatedDatapoint(object):
    """
    A timestamp-value pair returned for the specified request.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AggregatedDatapoint object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param timestamp:
            The value to assign to the timestamp property of this AggregatedDatapoint.
        :type timestamp: datetime

        :param value:
            The value to assign to the value property of this AggregatedDatapoint.
        :type value: float

        """
        self.swagger_types = {
            'timestamp': 'datetime',
            'value': 'float'
        }

        self.attribute_map = {
            'timestamp': 'timestamp',
            'value': 'value'
        }

        self._timestamp = None
        self._value = None

    @property
    def timestamp(self):
        """
        **[Required]** Gets the timestamp of this AggregatedDatapoint.
        The date and time associated with the value of this data point. Format defined by RFC3339.

        Example: `2019-02-01T01:02:29.600Z`


        :return: The timestamp of this AggregatedDatapoint.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this AggregatedDatapoint.
        The date and time associated with the value of this data point. Format defined by RFC3339.

        Example: `2019-02-01T01:02:29.600Z`


        :param timestamp: The timestamp of this AggregatedDatapoint.
        :type: datetime
        """
        self._timestamp = timestamp

    @property
    def value(self):
        """
        **[Required]** Gets the value of this AggregatedDatapoint.
        Numeric value of the metric.

        Example: `10.4`


        :return: The value of this AggregatedDatapoint.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this AggregatedDatapoint.
        Numeric value of the metric.

        Example: `10.4`


        :param value: The value of this AggregatedDatapoint.
        :type: float
        """
        self._value = value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
