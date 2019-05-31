"""
Common functionality for channel access.
"""

import enum
import math
from datetime import datetime, timedelta, timezone

from . import ca



def _create_enum(data):
    obj = enum.Enum(data[0], data[2])
    if data[1]:
        setattr(obj, '__doc__', data[1])
    return obj

def _create_flag(data):
    try:
        obj = enum.Flag(data[0], data[2])
    except AttributeError:
        # If the Flag class doesn't exist we fall back our own flag class
        from .flag import create_flag
        obj = create_flag(data[0], data[2])
    if data[1]:
        setattr(obj, '__doc__', data[1])
    return obj


Status = _create_enum(ca.Status)
Severity = _create_enum(ca.Severity)
Type = _create_enum(ca.Type)
AccessRights = _create_flag(ca.AccessRights)
Events = _create_flag(ca.Events)

#: Epics Epoch
EPICS_EPOCH = datetime.fromtimestamp(ca.EPICS_EPOCH, timezone.utc)

def datetime_to_epics(timestamp):
    """
    Convert a datetime object to an epics timestamp tuple.

    Args:
        timestamp (datetime): A datetime object. Is this is a naive
            datetime object the timezone is assumed to be UTC.

    Returns:
        A ``(seconds, nanoseconds)`` tuple with an origin of :py:data:`EPICS_EPOCH`
        in timezone UTC.
    """
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    posix = timestamp.astimezone(timezone.utc).timestamp()
    frac, sec = math.modf(posix)
    return (sec - ca.EPICS_EPOCH, int(frac * 1E9))

def epics_to_datetime(timestamp):
    """
    Convert an epics timestamp tuple to a datetime object.

    Args:
        timestamp: A ``(seconds, nanoseconds)`` tuple with an origin
            of :py:data:`EPICS_EPOCH` in timezone UTC.

    Returns:
        An aware datetime object with UTC timezone.
    """
    return datetime.fromtimestamp(ca.EPICS_EPOCH + timestamp[0] + timestamp[1] * 1E-9, timezone.utc)
