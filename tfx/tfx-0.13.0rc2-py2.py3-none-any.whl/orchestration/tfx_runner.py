# Copyright 2019 Google LLC. All Rights Reserved.
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
"""Definition of TFX runner base class."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
from six import with_metaclass


class TfxRunner(with_metaclass(abc.ABCMeta, object)):
  """Base runner class for TFX.

  This is the base class for every TFX runner.

  """

  @abc.abstractmethod
  def run(self, pipeline):
    """Runs logical TFX pipeline on specific platform.

    Args:
      pipeline: logical TFX pipeline definition.

    Returns:
      Platform-specific pipeline object.
    """
    pass
