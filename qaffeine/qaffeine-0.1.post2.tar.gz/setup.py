#!/usr/bin/env python3
#
# qaffeine - prevent inactivity on your computer by simulating key events
#
# Clem Lorteau - 2019-05-31

import setuptools
from src.__init__ import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'qaffeine',
    version = __version__ + '.post2',
    author = 'Clem Lorteau',
    author_email = 'clem@lorteau.fr',
    description = 'Prevent your computer from entering inactivity modes',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/clorteau/qaffeine',
    python_requires = '>=3',
    packages = setuptools.find_packages(),
    license = 'Unlicense',
    install_requires = [
        'PySide2',
        'autogui',
    ],
    package_data = {
        'src': [
            'res/*.ui',
            'res/*.png',
            'keys.txt',
            'LICENSE'
        ],
    },
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: Public Domain',
        'Operating System :: OS Independent',
    ],
    entry_points = {
        'gui_scripts': [
            'qaffeine = src.qaffeine:gui'
        ],
        'console_scripts': [
            'qaffeine-cli = src.qaffeine:cli'
        ]
    },
)
