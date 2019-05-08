#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

# To make a release follow these steps:
#   python setup.py sdist
#   twine upload dist/argos-0.2.0rc1.tar.gz

# See also https://packaging.python.org/en/latest/distributing.html
# TODO: still can't make a wheel even following the instructions in the link below.
# http://stackoverflow.com/questions/26664102/why-can-i-not-create-a-wheel-in-pyt

import sys

def err(*args, **kwargs):
    sys.stderr.write(*args, **kwargs)
    sys.stderr.write('\n')


try:
    from setuptools import setup, find_packages
except ImportError:
    err("Argos requires setuptools for intallation. (https://pythonhosted.org/an_example_pypi_project/setuptools.html)")
    err("You can download and install it simply with: python argos/external/ez_setup.py")
    sys.exit(1)


from argos import info

assert not info.DEBUGGING, "info.DEBUGGING must be False to make a release."

if sys.version_info < (2,7) or ((3,0) <= sys.version_info < (3, 4)):
    err("Arogs requires Python 2.7 and higher or 3.4 and higher.")
    sys.exit(1)


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

# From http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=install_requires#declaring-dependencies
# Using the install_requires option has three effects:
#  1) When your project is installed, either by using EasyInstall, setup.py install, or
#     setup.py develop, all of the dependencies not already installed will be located (via PyPI),
#     downloaded, built (if necessary), and installed.
#  2) Any scripts in your project will be installed with wrappers that verify the availability of
#     the specified dependencies at runtime, and ensure that the correct versions are added to
#     sys.path (e.g. if multiple versions have been installed).
#  3) Python Egg distributions will include a metadata file listing the dependencies.
#
# The reason for disabling install_requires is that, if a dependency is installed without pip or
# easy_install, the argos launcher script that is generated by setup.py gives the following error:
# pkg_resources.DistributionNotFound: The 'PyQt5' distribution was not found and is required by argos
# It was most likely caused by not having pip installed but it is unclear how to debug this and
# google didn't help. I don't know how to resolve these errors, so to save myself a lot of headaches
# I disabled automatic dependency installation.

# Declaring depdencies. DISABLED, see comment above.
install_requires = [
    "PyQt5 >= 5.6.0", # Don't know which version is minimal
    "numpy >= 1.11",
    # Argos will technically work without pyqtgraph and h5py, but with very limited functionality.
    "pyqtgraph >= 0.10",
    "h5py >= 2.6"
]


setup(
    name = info.REPO_NAME,
    version = info.VERSION,
    description = info.SHORT_DESCRIPTION,
    long_description = readme + '\n\n' + history,
    author = info.AUTHOR,
    author_email = info.EMAIL,
    license = "GPLv3",
    url=info.PROJECT_URL,
    packages = find_packages(),
    package_data = {'': ['HISTORY.rst'], info.PACKAGE_NAME: ['img/snipicons/*']},
    entry_points={'gui_scripts': ['argosge = argos.main:main']},
    #install_requires = install_requires, # DISABLED. See coments above.
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',
    ],
    keywords = 'NCDF HDF plotting graphs',
    #test_suite='tests',
    #tests_require=test_requirements
)
