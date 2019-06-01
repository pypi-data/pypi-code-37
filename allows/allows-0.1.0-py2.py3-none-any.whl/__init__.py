# -*- coding: utf-8 -*-

"""
Top-level package for Allows: a package for easier mock configuration and assertions
in Python.
"""

__all__ = [
    "allow",
    "return_value",
    "raise_exception",
    "receive_method",
    "be_called_with",
    "have_effect",
]

__author__ = """Dave Anderson"""
__email__ = "dave@dvndrsn.com"
__version__ = "0.1.0"

from .factory import (  # noqa: F401
    allow,
    return_value,
    return_,
    raise_exception,
    raise_,
    receive_method,
    receive,
    be_called_with,
    have_effect,
)
from .exception import AllowsException  # noqa: F401
from .side_effect import SideEffect, SideEffectBuilder  # noqa: F401
