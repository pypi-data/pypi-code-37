#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: sign.py
# @time: 2019/5/6 9:48
# @Software: PyCharm


__author__ = 'A.Star'

from abc import ABCMeta, abstractmethod
from astartool.random import random_hex_string
from pysmx.SM2 import Sign as sm2_sign
from pysmx.SM2 import Verify as sm2_verify
from pysmx.crypto import hashlib
import hmac

ALLOW_ALG = ['SM2', 'HS256', 'RS256', 'HSM3']


class Sign(metaclass=ABCMeta):
    name = 'BASE'

    @staticmethod
    @abstractmethod
    def signature(encoded_string, key, rand, len_param=64, encoding='utf-8', *args, **kwargs):
        pass


class SM2Sign(Sign):
    name = 'SM2'

    @staticmethod
    def signature(encoded_string, key, rand=None, len_param=64, encoding='utf-8', *args, **kwargs):
        assert isinstance(rand, str)
        assert isinstance(encoding, str)
        if rand is None:
            rand = random_hex_string(16)
        return sm2_sign(encoded_string, key, rand, len_para=len_param, encoding=encoding)


class HS256Sign(Sign):
    name = 'HS256'

    @staticmethod
    def signature(encoded_string, key, rand, len_param=64, encoding='utf-8', *args, **kwargs):
        assert isinstance(rand, str)
        assert isinstance(encoding, str)
        return hmac.new(key, encoded_string.encode(encoding), hashlib.sha256).digest()


class RS256Sign(Sign):
    name = 'RS256'

    @staticmethod
    def signature(encoded_string, key, rand, len_param=64, encoding='utf-8', *args, **kwargs):
        assert isinstance(rand, str)
        assert isinstance(encoding, str)
        raise NotImplementedError


class HSM3Sign(Sign):
    name = 'HSM3'

    @staticmethod
    def signature(encoded_string, key, rand, len_param=64, encoding='utf-8', *args, **kwargs):
        return hmac.new(key, encoded_string, hashlib.sm3).digest()


class Verify(metaclass=ABCMeta):
    name = 'BASE'

    @staticmethod
    @abstractmethod
    def verify(sign, message, key, len_param=64, *args, **kwargs):
        pass


class SM2Verify(Verify):
    name = 'SM2'

    @staticmethod
    def verify(sign, message, key, len_param=64, *args, **kwargs):
        return sm2_verify(sign, message, key, len_para=len_param)


class HS256Verify(Verify):
    name = 'HS256'

    @staticmethod
    def verify(sign, message, key, len_param=64, *args, **kwargs):
        return hmac.new(key, message, hashlib.sha256).digest() == sign


class RS256Verify(Verify):
    name = 'RS256'

    @staticmethod
    def verify(sign, message, key, len_param=64, *args, **kwargs):
        raise NotImplementedError


class HSM3Verify(Verify):
    name = 'HSM3'

    @staticmethod
    def verify(sign, message, key, len_param=64, *args, **kwargs):
        return hmac.new(key, message, hashlib.sm3).digest() == sign
