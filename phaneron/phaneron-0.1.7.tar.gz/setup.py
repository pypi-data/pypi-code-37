#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, Cyrille Favreau <cyrille.favreau@gmail.com>
#
# This file is part of pyPhaneron
# <https://github.com/favreau/pyPhaneron>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.

"""setup.py"""
import re
from setuptools import setup
from phaneron.version import __version__

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


VERSIONFILE = "phaneron/version.py"
ver_file = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, ver_file, re.M)

if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

install_reqs = parse_requirements('requirements.txt')
reqs = install_reqs

setup(name='phaneron',
      version=__version__,
      description='Helper function for Phaneron',
      packages=['phaneron'],
      url='https://github.com/favreau/pyPhaneron.git',
      author='Cyrille Favreau',
      author_email='cyrille.favreau@gmail.com',
      license='GNU LGPL',
      install_requires=reqs,)
