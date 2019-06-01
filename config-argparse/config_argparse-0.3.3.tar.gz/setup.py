#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='config_argparse',
    version='0.3.3',
    description='config library based on standard ArgumentParser',
    author='cormoran',
    author_email='cormoran707@gmail.com',
    url='https://github.com/cormoran/config_argparse',
    license='mit',
    packages=find_packages(exclude=('tests')),
    install_requires=[],
    test_suite='tests',
)