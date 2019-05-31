#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="mulpy",
    version="0.0.3",
    author="Asakawa Rikka",
    author_email="AsakawaRikka@gmail.com",
    description="A user-friendly Python concurrency control package.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/",
    packages=['mulpy'],
    platforms=['any'],
    install_requires=[
    ],
    classifiers=[],
)
