#!/usr/bin/env python3

import setuptools
import __init__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'qaffeine',
    version = __init__.__version__,
    author = 'Clem Lorteau',
    author_email = 'clem@lorteau.fr',
    description = 'Prevent your computer from entering inactivity modes',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/clorteau/qaffeine',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: Public Domain',
        'Operating System :: OS Independent',
    ]
)
