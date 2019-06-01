#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_music',
      version='1.0.4',
      description='search music',
      long_description='search music',
      author='mengxf',
      author_email='mengxf01@fenbi.com',
      keywords=['python', 'music'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_music'],
      package_data={'ybc_music': ['*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_exception', 'pycrypto']
      )