#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requires = [
    'setuptools',
    'pyhasse.core'
]


setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Rainer Bruggemann",
    author_email='rainer.bruggemann@pyhasse.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="pyhasse-fuzzy: Concept of De Walle et al […], where the relations between two objects are evaluated by fuzzy techniques.",
    install_requires=requires,
    license="MIT license",
    long_description_content_type='text/x-rst',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fuzzy',
    packages=['pyhasse.fuzzy'],
    namespace_packages=['pyhasse'],
    name='pyhasse.fuzzy',
    package_dir={'': 'src'},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://bitbucket.com/brg/fuzzy',
    version='0.1.1',
    zip_safe=False,
)
