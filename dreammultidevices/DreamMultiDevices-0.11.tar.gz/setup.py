#!/usr/bin/env python

import re
import setuptools

version = "0.11"

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="DreamMultiDevices",
    version=version,
    author="无声andTreize",
    author_email="saint_228@126.com",
    description="Simple Automated Testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saint228/DreamMultiDevices",
    install_requires=[
        'airtest>=1.0.26',
        'BeautifulReport>=0.0.9',
        'pocoui>=1.0.76',
    ],
    packages=setuptools.find_packages(),
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ),

)