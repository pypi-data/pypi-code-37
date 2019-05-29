#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bottle-mold removes the need to repeat boilerplate code for your bottle services.
Python Standard Library.
Copyright (c) 2019, James Burke.
License: MIT (see LICENSE for details)
"""

__author__ = 'James Burke'
__version__ = '0.0.3.dev1'
__license__ = 'MIT'

import bottle

import logging
import decimal
import datetime
import os
import sys

SUPPORTED_ORM = (None, 'sqlalchemy',)
BOTTLE_FUNCTIONS = ('template', 'TEMPLATE_PATH', 'static_file',
                    'response', 'request', 'error',)

logger = logging.getLogger(__name__)

class Mold(bottle.Bottle):

    def __init__(self):
        bottle.Bottle.__init__(self, catchall=True)
       
        if os.environ.get("DATABASE_ORM") not in SUPPORTED_ORM:
            raise Exception("Unsupported ORM - {}".format(os.environ.get("DATABASE_ORM")))
        elif os.environ.get("DATABASE_ORM") == 'sqlalchemy':
            import sqlalchemy
            from sqlalchemy import create_engine
            from bottle.ext import sqlalchemy as bottle_sqlalchemy
            from sqlalchemy.ext.declarative import declarative_base

            engine = create_engine(os.environ['DATABASE_CONNECTION_STRING'],
                echo=False
            )
            self.install(bottle_sqlalchemy.Plugin(engine, keyword="db"))

            self.alchemyencoder = alchemyencoder

            self.base = declarative_base()

        # Enable CORS
        if os.environ.get("CORS_URL"):
            self.install(EnableCors())

        # Load helpful bottle functions
        for bottle_function in BOTTLE_FUNCTIONS:
            print(bottle_function)
            setattr(self, bottle_function, getattr(bottle, bottle_function))


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            bottle.response.headers['Access-Control-Allow-Origin'] = os.environ["CORS_URL"]
            bottle.response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE, OPTIONS"
            bottle.response.headers['Access-Control-Allow-Headers'] = \
                "Origin, Accept, Authorization, Content-Type, X-Requested-With, X-CSRF-Token"
            bottle.response.headers['Access-Control-Allow-Credentials'] = "true"
            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


def alchemyencoder(self, obj):
    """
    JSON encoder function for SQLAlchemy special classes.
     - timestamps
     - decimals
    """
    if isinstance(obj, datetime.date):
        try:
            utcoffset = obj.utcoffset() or datetime.timedelta(0)
            return (obj - utcoffset).strftime('%Y-%m-%d %H:%M:%S')
        except AttributeError:
            return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
