#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: token.py
# @time: 2019/3/19 10:40
# @Software: PyCharm

import datetime
import json
from snowland_authsdk.common import SNOWLAND_ACCOUNT_ISS, SNOWLAND_PUBLIC_KEY
import requests
from snowland_authsdk.key_store import get_publickey
from base64 import urlsafe_b64encode, urlsafe_b64decode
# from pysmx.SM2 import Sign, Verify
from snowland_authsdk.util import random_hex_string
from snowland_authsdk.decorator import token_timeout
from snowland_authsdk.sign import *

__author__ = 'A.Star'

ALLOW_ALG = ['SM2', 'HS256', 'RS256', 'HSM3']


def generate_token(payload: dict, secret=None, k=32, len_param=64, encoding='utf-8', alg='SM2', rand=None, *,
                   typ=b'JWT', **kwargs):
    """
    生成token, JWT 标准,
    参考： https://ninghao.net/blog/2834
    :param payload: dict 验证token时需要返回的信息
    :param secret: 私钥
    :param k: 16进制随机数的长度
    :param len_param: SM2签名参数，目前只支持64
    :param encoding: 编码
    :param alg: 算法
    :return: token
    """
    assert len_param == 64
    if isinstance(alg, type) and issubclass(alg, Sign):
        header = b'{"alg":"%s","typ":"%s"}' % (bytes(alg.name, encoding), typ)
        SignAlgorithm = alg
    else:
        if isinstance(alg, str):
            header = b'{"alg":"%s","typ":"%s"}' % (bytes(alg, encoding), typ)
        elif isinstance(alg, (bytes, bytearray)):
            header = b'{"alg":"%s","typ":"%s"}' % (alg, typ)
            alg = str(alg, encoding=encoding)
        assert alg in ALLOW_ALG
        if alg == 'SM2':
            SignAlgorithm = SM2Sign
        elif alg == 'HS256':
            SignAlgorithm = HS256Sign
        elif alg == 'RS256':
            SignAlgorithm = RS256Sign
        elif alg == 'HSM3':
            SignAlgorithm = HSM3Sign
        else:
            return None
    rand = payload.get('rand', None) or rand
    if rand is None:
        rand = random_hex_string(k)
    if isinstance(rand, (bytes, bytearray)):
        rand = str(rand, encoding=encoding)
    payload['rand'] = rand

    payload = bytes(json.dumps(payload), encoding=encoding)
    encoded_string = urlsafe_b64encode(header) + b"." + urlsafe_b64encode(payload)
    signed = SignAlgorithm.signature(str(encoded_string, encoding=encoding), secret, rand, len_para=len_param)
    assert isinstance(signed, (bytes, bytearray))
    b = encoded_string + b'.' + urlsafe_b64encode(signed)
    return str(b, encoding=encoding)


def verify_token(token: (bytes, str), publickey, len_param=64, expire_seconds=3600, *, encoding='utf-8',
                 allow_timeout=True, **kwargs):
    """
    验证token有效性
    :param token: generate_token生成的token
    :param publickey: 公钥
    :param len_param: 密钥长度
    :param expire_seconds: 过期时间（秒记）
    :return: 如果token无效，返回None,否则返回header, payload
    """
    try:
        if isinstance(token, str):
            token = bytes(token, encoding=encoding)
        split_token = token.split(b'.')
        assert len(split_token) == 3
        header = json.loads(urlsafe_b64decode(split_token[0]))
        payload = json.loads(urlsafe_b64decode(split_token[1]))
        e = split_token[0] + b'.' + split_token[1]
        alg = header['alg'].upper()
        assert alg in ALLOW_ALG
        if alg == 'SM2':
            VerifyAlgorithm = SM2Verify
        elif alg == 'HS256':
            VerifyAlgorithm = HS256Verify
        elif alg == 'RS256':
            VerifyAlgorithm = RS256Verify
        elif alg == 'HSM3':
            VerifyAlgorithm = HSM3Verify
        else:
            return None
        signed = urlsafe_b64decode(split_token[2])
        # 签名检验
        # print("verify:", signed)
        # print("v-rand:", payload['rand'])
        if not VerifyAlgorithm.verify(signed, e, publickey, len_param):
            return None
        if allow_timeout and not token_timeout(payload, expire_seconds=expire_seconds):
            return None
        return header, payload
    except:
        return None


def verify_token_by_uri(token: (bytes, str), len_param=64, expire_seconds=300, *, encoding='utf-8', allow_timeout=True):
    """
    验证token有效性
    :param token: generate_token生成的token
    :param len_param: 密钥长度
    :param expire_seconds: 过期时间（秒记）
    :param encoding: 字符串编码方式
    :return: 如果token无效，返回None,否则返回header, payload
    """
    try:
        if isinstance(token, str):
            token = bytes(token, encoding=encoding)
        split_token = token.split(b'.')
        assert len(split_token) == 3
        header = json.loads(urlsafe_b64decode(split_token[0]))
        payload = json.loads(urlsafe_b64decode(split_token[1]))
        e = split_token[0] + b'.' + split_token[1]
        alg = header['alg'].upper()
        assert alg in ALLOW_ALG
        if alg == 'SM2':
            VerifyAlgorithm = SM2Verify
        elif alg == 'HS256':
            VerifyAlgorithm = HS256Verify
        elif alg == 'RS256':
            VerifyAlgorithm = RS256Verify
        elif alg == 'HSM3':
            VerifyAlgorithm = HSM3Verify
        else:
            return None
        signed = str(urlsafe_b64decode(split_token[2]), encoding=encoding)
        # 签名检验
        # print("verify:", signed)
        # print("v-rand:", payload['rand'])
        if payload['iss'] == SNOWLAND_ACCOUNT_ISS:
            if VerifyAlgorithm.verify(signed, e, SNOWLAND_PUBLIC_KEY, len_param):
                return payload
            else:
                return None
        else:
            publickey_json = get_publickey(payload['iss'])
            if publickey_json is not None and publickey_json['successful']:
                publickey = publickey_json['data']['publickey']
                if not VerifyAlgorithm.verify(signed, e, publickey, len_param):
                    return None
                if allow_timeout and not token_timeout(payload, expire_seconds=expire_seconds):
                    return None
            else:
                return None
        return header, payload
    except:
        return None
