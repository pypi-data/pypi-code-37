# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

_package_data = dict(
    full_package_name='ruamel.music',
    version_info=(0, 3, 7),
    __version__='0.3.7',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='handling of music files: conversion, playing',
    toxver=['2.7'],
    entry_points=['music = ruamel.music.__main__:main'],
    install_requires=[
            'ruamel.appconfig',
            'ruamel.std.argparse>=0.8',
            'mutagen',
            'musicbrainzngs',
            'ruamel.yaml',
            'ruamel.doc.html',
            'ruamel.std.pathlib;python_version<"3.0"',
    ],
    license='Copyright Ruamel bvba 2013-2015',
    # status= "α",
    # data_files= "",
    # universal= 1,
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']
