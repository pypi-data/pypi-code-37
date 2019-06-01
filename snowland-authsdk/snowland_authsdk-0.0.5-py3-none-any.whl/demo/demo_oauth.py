#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: demo_oauth.py
# @time: 2019/3/15 10:11
# @Software: PyCharm


__author__ = 'A.Star'

from snowland_authsdk.login import OAuth
import json

# DEMO
# access_key = 'tuxf517fqdserop68z1m3zmf6bs6tkrf'
# access_secret = '2446ea7d1722da461052d547268480b5aca159a781ccba27908a3acde887889c'
# public key = 'f5d15acf5a1e9c75a23c2d8db5bf9b6425137b23a8ec270a097d2e585e243c6ddc8b53cc385ebdaa2dc1b20b4f0d0b56b1a678af42005a1cecacc7631b999186'

# 测试使用
access_key = 'i76viekv2i36v0cx6di2c6gvnjrn4ah7'
access_secret = '22f578accc91993da8d95bba210a111c88632424329e05f691f3b07275a8347b'


app = OAuth(access_key, access_secret)

user = {
    "username": "test",
    "password": "try_Test_123"
}

application = access_key

param = {
    "application": application
}

res = app.oauth_authorize(**param, **user)
print("auth:", res)
# code = input('code=')
code = json.loads(res)['data']['code']
res = app.oauth_access_token(**{"code": code, "method":'post'})
print("token-post:", res)
# res = app.oauth_access_token(**{"code": code, "method": 'get'})
# print("token-get:", res)
# token = input('token=')
token = json.loads(res)['data']['token']
print("userinfo:", app.oauth_userinfo(**{"token":token}))

