#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""UVSnap Module Constants."""

import logging

__author__ = 'Greg Albrecht <oss@undef.net>'
__copyright__ = 'Copyright 2017 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


LOG_LEVEL = logging.INFO
LOG_FORMAT = logging.Formatter(
    ('%(asctime)s uvsnap %(levelname)s %(name)s.%(funcName)s:%(lineno)d - '
     '%(message)s'))
