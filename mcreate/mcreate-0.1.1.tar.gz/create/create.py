# -*- coding: utf-8 -*-

"""Main module."""

import configparser
import os
cp = configparser.ConfigParser()
txtpath = os.path.dirname(os.path.abspath(__file__))+'/config.txt'
try:
    with open(txtpath) as f:
        cp.read_file(f)
        token = cp.get('Config','password') 
        print(token)
except:
    cfgfile = open(txtpath,'w')
    cp.add_section('Config')
    token = str(input('There are no saved Github access tokens saved.\nPlease enter your Github token: '))
    cp.set('Config','password',token)
    cp.write(cfgfile)
    cfgfile.close()