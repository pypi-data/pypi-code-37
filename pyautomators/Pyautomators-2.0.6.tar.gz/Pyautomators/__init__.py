# -*- coding: UTF-8 -*-
"""Pyautomators is behaviour-driven development, Python style

Behavior-driven development (or BDD) is an agile software development
technique that encourages collaboration between developers, QA and
non-technical or business participants in a software project.

*Pyautomators* uses tests written in a natural language style, backed up by Python
code.

To get started, we recommend the `tutorial`_ and then the `test language`_ and
`api`_ references.

.. _`tutorial`: tutorial.html
.. _`test language`: gherkin.html
.. _`api`: api.html
"""

from __future__ import absolute_import
from Pyautomators.step_registry import *      # pylint: disable=wildcard-import
from Pyautomators.matchers import use_step_matcher, step_matcher, register_type
from Pyautomators.fixture import fixture, use_fixture

# pylint: disable=undefined-all-variable
__all__ = [
    "given", "when", "then", "step", "use_step_matcher", "register_type",
    "Given", "When", "Then", "Step",
    "fixture", "use_fixture",
    # -- DEPRECATING:
    "step_matcher"
]
__version__ = "2.0.5"
