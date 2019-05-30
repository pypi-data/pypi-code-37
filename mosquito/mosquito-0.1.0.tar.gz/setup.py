#!/usr/bin/env python3

# Standard library modules.
import os

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASEDIR, 'README.md'), 'r') as fp:
    LONG_DESCRIPTION = fp.read()

PACKAGES = find_packages()

INSTALL_REQUIRES = ['requests', 'tqdm']
EXTRAS_REQUIRE = {'develop': ['nose']}

ENTRY_POINTS = {}

setup(
    name='mosquito',
    version='0.1.0',
    author="luoc",
    author_email="luoc@posteo.org",
    description="a request obfuscator and web scraping toolkit",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://luoc.eu",
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    test_suite='nose.collector',
    scripts=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
