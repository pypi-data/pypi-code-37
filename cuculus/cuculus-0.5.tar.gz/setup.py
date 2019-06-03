#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='cuculus',
    version=0.5,
    description=(
        'Culusus Logging Client'
    ),
    long_description=open('README.rst').read(),
    author='Chris Hwang',
    author_email='chrishwang@live.cn',
    maintainer='Chris',
    maintainer_email='chrishwang@live.cn',
    license='BSD License',
    #packages=find_packages(),
    packages=['cuculus'],
    platforms=["all"],
    url='https://github.com/aolyn',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)
