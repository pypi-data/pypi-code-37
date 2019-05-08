#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2018.11.28

vlogs = {
    '0.0.8': 'add text search template',
    '0.0.9': 'update service template url; auto check version',
    '0.1.0': 'add go source file wathdog',
    '0.1.1': 'add api version',
    '0.1.2': 'fix page',
    '0.1.3': 'add string type or/like template, fix without manager query bug',
    '0.1.4': 'update watchgo/orm',
    '0.1.5': 'update swagger',
    '0.1.6': 'fix manager list relation',
    '0.1.7': 'fix with string like',
    '0.1.8': 'page 1 base: 注意当前版本分页功能从1开始, 应用层不需要再做pageIndex-1 操作!!!' # add change_log notify
}

name = 'm2c'
version = '0.1.8'

from .conf import M2C_PATH, Color
from .helper import m2c_version

def change_log():
    curv = m2c_version()
    if not curv:
        return

    if curv == version:
        return

    print Color.red(u'当前项目使用的m2c版本: %s' % curv)
    print Color.red(u'使用m2c apicode 或者m2c objcode 可以更新当前版本')
    print Color.red(u'注意以下更新:')
    for v, msg in vlogs.iteritems():
        if v > curv:
            print v, msg


def check_version():
    import os
    from .conf import Color
    change_log()
    text = os.popen('pip search %s' % name).read()
    need_update = False
    for line in text.splitlines():
        print line
        line = line.strip()
        if line.startswith('LATEST:'):
            need_update = True
    if need_update:
        print Color.red('run: pip install -U %s, update it!' % name)
