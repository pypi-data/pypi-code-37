#!/usr/bin/env python3

## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at https://mozilla.org/MPL/2.0/.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="staticgen",
    version="0.0.1",
    author="Eduardo Rolim",
    author_email="ens.rolim@gmail.com",
    description="A simple static site generation tool",
    license='MPLv2',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ens.rolim/staticgen.py",
    packages=["staticgen"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English",
        "Natural Language :: Portuguese (Brazilian)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Code Generators",
    ],
)
