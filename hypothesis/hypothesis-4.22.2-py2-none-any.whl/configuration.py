# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2019 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import absolute_import, division, print_function

import os

__hypothesis_home_directory_default = os.path.join(os.getcwd(), ".hypothesis")

__hypothesis_home_directory = None


def set_hypothesis_home_dir(directory):
    global __hypothesis_home_directory
    __hypothesis_home_directory = directory


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def hypothesis_home_dir():
    global __hypothesis_home_directory
    if not __hypothesis_home_directory:
        __hypothesis_home_directory = os.getenv("HYPOTHESIS_STORAGE_DIRECTORY")
    if not __hypothesis_home_directory:
        __hypothesis_home_directory = __hypothesis_home_directory_default
        mkdir_p(__hypothesis_home_directory)
    return __hypothesis_home_directory


def storage_directory(*names):
    path = os.path.join(hypothesis_home_dir(), *names)
    mkdir_p(path)
    return path


def tmpdir():
    return storage_directory("tmp")
