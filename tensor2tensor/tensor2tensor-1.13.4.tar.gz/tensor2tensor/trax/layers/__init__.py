# coding=utf-8
# Copyright 2019 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Layers defined in trax."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# We create a flat layers.* namespace for uniform calling conventions as we
# upstream changes.
# pylint: disable=wildcard-import
from tensor2tensor.trax.layers.attention import *
from tensor2tensor.trax.layers.base import *
from tensor2tensor.trax.layers.combinators import *
from tensor2tensor.trax.layers.convolution import *
from tensor2tensor.trax.layers.core import *
from tensor2tensor.trax.layers.initializers import *
from tensor2tensor.trax.layers.normalization import *
from tensor2tensor.trax.layers.pooling import *
from tensor2tensor.trax.layers.rnn import *
