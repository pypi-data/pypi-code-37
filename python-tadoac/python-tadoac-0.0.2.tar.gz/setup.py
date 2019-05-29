#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

here = lambda *a: os.path.join(os.path.dirname(__file__), *a)

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open(here('README.md')).read()
requirements = [x.strip() for x in open(here('requirements.txt')).readlines()]

setup(name='python-tadoac',
      version='0.0.2',
      description='PyTado modified by dgaust for AC',
      long_description=readme,
      keywords='tado',
      author='dgaust',
      author_email='dgaust@outlook.com',
      url='https://github.com/dgaust/PyTado',
      install_requires=requirements,
      license="GPL3",
      zip_safe=False,
      platforms=["any"],
      packages=find_packages(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Home Automation',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5'
      ],
      entry_points={
        'console_scripts': [
            'PytadoAC = pytado.__main__:main'
        ]
      },
)
