from typing import Optional
from cmdi import CmdResult, command, set_result, strip_args

from . import lib


@command
def push_to_gemfury(
    wheel_file: str,
    **cmdargs,
) -> CmdResult:
    lib.push_to_gemfury(**strip_args(locals()))
    return set_result()


@command
def push(
    repository='pypi',
    clean_dir: bool = False,
    **cmdargs,
) -> CmdResult:
    lib.push(**strip_args(locals()))
    return set_result()


@command
def build(
    clean_dir: bool = False,
    **cmdargs,
) -> CmdResult:
    lib.build(**strip_args(locals()))
    return set_result()
