from typing import Optional
from cmdi import command, CmdResult, set_result, strip_args

from . import lib


@command
def add_all(**cmdargs) -> CmdResult:
    lib.add_all()
    return set_result()


@command
def commit(
    msg: str,
    **cmdargs,
) -> CmdResult:
    lib.commit(**strip_args(locals()))
    return set_result()


@command
def tag(
    version: str,
    branch: str,
    **cmdargs,
) -> CmdResult:
    lib.tag(**strip_args(locals()))
    return set_result()


@command
def push(
    branch: str,
    **cmdargs,
) -> CmdResult:
    lib.push(**strip_args(locals()))
    return set_result()


@command
def get_default_branch(**cmdargs) -> CmdResult:
    return set_result(lib.get_default_branch())


@command
def status(**cmdargs) -> CmdResult:
    lib.status()
    return set_result()


@command
def diff(**cmdargs) -> CmdResult:
    lib.diff()
    return set_result()
