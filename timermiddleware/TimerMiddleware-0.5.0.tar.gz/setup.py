from __future__ import absolute_import
from __future__ import unicode_literals
import sys
from setuptools import setup

py_version = sys.version_info[:2]

tests_require = ['nose']

if py_version[0] == 2:
    tests_require.append('mock')

setup(name='TimerMiddleware',
      version='0.5.0',
      url='http://sourceforge.net/p/timermiddleware',
      description='add timing instrumentation to WSGI applications',
      long_description='TimerMiddleware is a Python package for adding timing instrumentation to WSGI applications.',
      packages=['timermiddleware'],
      install_requires=['webob', 'future'],
      tests_require=tests_require,
      license='Apache 2.0',
      classifiers=[
          #  From http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: System :: Benchmark',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
      ],
)
