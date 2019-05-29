#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import pymagcore

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pymagcore",
    version='0.1.0',
    author="Miracle",
    author_email="miracleyoung0723@gmail.com",
    description="程序员的战争",
    long_description=' ',
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/MiracleYoung/You-are-Pythonista",
    packages=find_packages(),
    install_requires=[ 
        "requests",
    ],
    classifiers=[
        "Topic :: Games/Entertainment ",
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Games/Entertainment :: Board Games',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
