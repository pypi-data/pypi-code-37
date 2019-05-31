#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="mulpy",
    version="0.0.1",
    author="Asakawa Rikka",
    author_email="AsakawaRikka@gmail.com",
    description="A user-friendly Python concurrency control package.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/",
    packages=['mulpy'],
    install_requires=[
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
)
