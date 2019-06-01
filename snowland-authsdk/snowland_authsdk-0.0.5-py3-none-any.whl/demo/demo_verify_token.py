#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: demo_verify_token.py
# @time: 2019/5/9 10:08
# @Software: PyCharm


__author__ = 'A.Star'

from snowland_authsdk.token_helper import verify_token_by_uri, verify_token, generate_token
from snowland_authsdk.common import SNOWLAND_PUBLIC_KEY
from pysmx.SM2 import generate_keypair

if __name__ == '__main__':
    token = "eyJhbGciOiJTTTIifQ==.eyJpc3MiOiAiXHU2Y2IzXHU1MzE3XHU5NmVhXHU1N2RmXHU3ZjUxXHU3ZWRjXHU3OWQxXHU2MjgwXHU2NzA5XHU5NjUwXHU1MTZjXHU1M2Y4XHU4YmE0XHU4YmMxXHU1ZTczXHU1M2YwIiwgInN1YiI6ICJvYXV0aCAyLjAtcmVxdWlyZV9jb2RlIiwgImF1ZCI6ICJoYmN4dnJrdWxjcnFhbmJkOWJ6NzQxOGk3eXR6cnc1cSIsICJleHAiOiAiMjAxOS0wNS0wOSAxMDoxMDo0OCIsICJuYmYiOiAiMjAxOS0wNS0wOSAxMDowNTo0OCIsICJpYXQiOiAiMjAxOS0wNS0wOSAxMDowNTo0OCIsICJqdGkiOiBudWxsLCAiZGF0YSI6IHsiYXBwbGljYXRpb24iOiAiaTc2dmlla3YyaTM2djBjeDZkaTJjNmd2bmpybjRhaDcifSwgInJhbmQiOiAiNmU3M2QxZjUzY2Q4NzA4YmM0NjM1YWNlNTlhZjI5NTgifQ==.YmMxMTY2N2NkODA5MzkxZWI3NTUwNDdiMjY3Zjc1YThiYWY5MGMwNjc4ZjAzNWViOThlNzMwZGU1ZjM0MjRmYjMxMzQ4Mjg5OWM4ODI0MjBhNGNmNmJiZmQ2OTQwZGM0MWNmZmU4YTIwYTk4ZDVkNzU4YmQwMGEzMjUzMmE4ZmM="
    # print(verify_token_by_uri(token))
    # print(verify_token(token, SNOWLAND_PUBLIC_KEY))  # 因为超期而返回None
    algs = ALLOW_ALG = ['SM2', 'HS256', 'HSM3']
    msg = {"inf": "hello"}

    for alg in algs:
        pk, sk = generate_keypair()
        if alg in ['HS256', 'HSM3']:
            pk = sk
        token = generate_token(msg, sk, alg=alg)
        assert token is not None
        flag = verify_token(token.encode(), pk, alg=alg, allow_timeout=False)
        print(flag is not None)
