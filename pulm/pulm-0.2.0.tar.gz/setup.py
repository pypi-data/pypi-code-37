# -*- coding: utf-8 -*-
import re

import setuptools
import os

with open(os.path.join("pulm","pulm.py")) as fh:
    version = re.search('^__version__\s*=\s*"(.*)"', fh.read(), re.M).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pulm",
    packages = ["pulm"],
    entry_points = {
        "console_scripts": ['pulm = pulm.pulm:main']
    },
    version=version,
    author="Julien Jerphanion",
    author_email="git@jjerphan.xyz",
    description="PlantUML script generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjerphan/pulm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
