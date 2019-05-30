#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for UVSnap

Source:: https://github.com/ampledata/uvsnap
"""

import os
import sys

import setuptools

__title__ = 'uvsnap'
__version__ = '2.0.0'
__author__ = 'Greg Albrecht <oss@undef.net>'
__copyright__ = 'Copyright 2019 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')
        sys.exit()


publish()


setuptools.setup(
    name=__title__,
    version=__version__,
    description='UVSnap: UniFi Video Command Line Client',
    author='Greg Albrecht',
    author_email='oss@undef.net',
    packages=['uvsnap'],
    package_data={'': ['LICENSE']},
    package_dir={'uvsnap': 'uvsnap'},
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/ampledata/uvsnap',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'requests >= 2.7.0'
    ],
    entry_points={'console_scripts': ['uvsnap = uvsnap.cmd:cli']}

)
