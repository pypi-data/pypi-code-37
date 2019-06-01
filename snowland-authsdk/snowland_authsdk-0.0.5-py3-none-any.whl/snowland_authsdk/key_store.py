#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: key_store.py
# @time: 2019/5/7 9:06
# @Software: PyCharm


__author__ = 'A.Star'

import requests
from snowland_authsdk.common import PUBLIC_KEY_URL


def get_publickey(access_key):
    try:
        res = requests.get(PUBLIC_KEY_URL, params={"access_key": access_key})
        return res.json()
    except:
        return None
