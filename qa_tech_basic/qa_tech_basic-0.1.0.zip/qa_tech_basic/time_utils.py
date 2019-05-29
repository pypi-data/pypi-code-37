# -*- coding: utf-8 -*-
# author:      hj
# create_time: 2019/5/24 16:50
# update_time: 2019/5/24 16:50
import datetime
import time


class TimeUtils(object):
    """
    时间辅助类
    """
    DEFAULT_PATTERN = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def get_now_stamp(millisecond=False):
        """
        获取当前系统日期的时间戳：默认至秒
        :param millisecond: 是否需要毫秒
        :return:
        """
        now = int(time.time())
        if millisecond:
            return now*1000
        return now

    @staticmethod
    def get_now_str(_pattern=DEFAULT_PATTERN):
        """
        根据指定格式，返回string类型的当前系统日期
        :param _pattern:
        :return:
        """
        return time.strftime(_pattern, time.localtime())

    @staticmethod
    def parse_str_time(str_time, _pattern=DEFAULT_PATTERN):
        """
        将字符串转为time对象
        :param str_time: string time
        :param _pattern: string time对应的格式
        :return:
        """
        return time.strptime(str_time, _pattern)

    @staticmethod
    def parse_str_datetime(str_time, _pattern=DEFAULT_PATTERN):
        """
        将字符串转为datetime对象
        :param str_time:
        :param _pattern:
        :return:
        """
        return datetime.datetime.strptime(str_time, _pattern)

    @staticmethod
    def parse_str_timestamp(str_time, _pattern=DEFAULT_PATTERN):
        """
        将字符串时间转为时间戳
        :param str_time: string time
        :param _pattern: string time 对应格式
        :return:
        """
        return time.mktime(TimeUtils.parse_str_time(str_time, _pattern))

    @staticmethod
    def format_str_str(raw_str_time, raw_str_pattern, new_str_pattern):
        """
        将字符串时间格式转为另一种格式字符串
        :param raw_str_time: 原字符串
        :param raw_str_pattern: 原字符串格式
        :param new_str_pattern: 新字符串格式
        :return:
        """
        p_time = time.strptime(raw_str_time, raw_str_pattern)
        return time.strftime(new_str_pattern, p_time)

    @staticmethod
    def delta_datetime(_time, format_pattern=DEFAULT_PATTERN, years=0, days=0, hours=0, minutes=0):
        """
        时间处理：正数在时间维度上增加，负数，在时间维度上减少
        :param _time: datetime
        :param format_pattern: 将转为的时间格式
        :param years:
        :param days:
        :param hours:
        :param minutes:
        :return:
        """
        if not type(_time) == datetime.datetime:
            raise RuntimeError('The delta time, must be datetime instantiation.')
        _time1 = _time
        if years != 0:
            _time1 = _time1 + datetime.timedelta(days=int(years)*365)
        if days != 0:
            _time1 = _time1 + datetime.timedelta(days=int(days))
        if hours != 0:
            _time1 = _time1 + datetime.timedelta(days=int(hours))
        if minutes != 0:
            _time1 = _time1 + datetime.timedelta(days=int(minutes))
        return _time1.strftime(format_pattern)


if __name__ == '__main__':
    # print TimeUtils.parse_str_timestamp('2009-08-07', '%Y-%m-%d')
    # # 字符串时间格式转变
    # print TimeUtils.format_str_str('2009-08-07 01:02:13', '%Y-%m-%d %H:%M:%S', '%Y--%m--%d %H::%M::%S')
    # print datetime.datetime.now()
    dt = TimeUtils.parse_str_datetime('2009-08-07 01:02:13', '%Y-%m-%d %H:%M:%S')
    # 减少一年
    print TimeUtils.delta_datetime(dt,  '%Y-%m-%d %H:%M:%S', years=-1)
    # 增加10天
    print TimeUtils.delta_datetime(dt, '%Y-%m-%d %H:%M:%S', days=10)
    # 增加1年零十天
    print TimeUtils.delta_datetime(dt, '%Y-%m-%d', years=1, days=10)