#!/usr/bin/env python
# -*- coding: utf8 -*-
# Author: Tony <stayblank@gmail.com>
# Create: 2019/5/26 21:57
import time
from datetime import datetime

__all__ = ["TimeKong"]


class TimeKong(object):
    NANOSECOND = 1 / 1e9
    MICROSECOND = 1 / 1e6
    MILLISECOND = 1 / 1e3
    SECOND = 1
    MINUTE = 60
    HOUR = 60 * 60
    DAY = 24 * 60 * 60
    WEEK = 7 * 24 * 60 * 60
    MONTH = 31 * 24 * 60 * 60
    YEAR = 365 * 24 * 60 * 60

    FORMATTER = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def timestamp2datetime(timestamp, tz=None):
        return datetime.fromtimestamp(timestamp, tz=tz)

    @classmethod
    def timestamp2string(cls, timestamp, formatter=None):
        d = cls.timestamp2datetime(timestamp)
        return cls.datetime2string(d, formatter)

    @staticmethod
    def datetime2timestamp(d):
        a = time.mktime(d.timetuple())
        b = d.microsecond / 1e6
        return a + b

    @classmethod
    def datetime2string(cls, d, formatter=None):
        formatter = formatter or cls.FORMATTER
        return d.strftime(formatter)

    @classmethod
    def string2timestamp(cls, s, formatter=None):
        d = cls.string2datetime(s, formatter)
        return cls.datetime2timestamp(d)

    @classmethod
    def string2datetime(cls, s, formatter=None):
        formatter = formatter or cls.FORMATTER
        return datetime.strptime(s, formatter)

    @classmethod
    def floor_to_microsecond(cls, timestamp):
        return round(timestamp, 6)

    @classmethod
    def floor_to_millisecond(cls, timestamp):
        return round(timestamp, 3)

    @classmethod
    def floor_to_second(cls, timestamp):
        return round(timestamp, 1)

    @classmethod
    def floor_to_minute(cls, timestamp):
        return timestamp - timestamp % TimeKong.MINUTE

    @classmethod
    def floor_to_hour(cls, timestamp):
        return timestamp - timestamp % TimeKong.HOUR

    @classmethod
    def floor_to_day(cls, timestamp):
        d = cls.timestamp2datetime(timestamp)
        floor_d = datetime(year=d.year, month=d.month, day=d.day)
        return cls.datetime2timestamp(floor_d)

    @classmethod
    def floor_to_month(cls, timestamp):
        d = cls.timestamp2datetime(timestamp)
        floor_d = datetime(year=d.year, month=d.month, day=1)
        return cls.datetime2timestamp(floor_d)

    @classmethod
    def floor_to_year(cls, timestamp):
        d = cls.timestamp2datetime(timestamp)
        floor_d = datetime(year=d.year, month=1, day=1)
        return cls.datetime2timestamp(floor_d)
