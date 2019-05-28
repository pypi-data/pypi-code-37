from cmdi import CmdResult, command, set_result, strip_args

from . import lib


@command
def bump_version(
    semver_num: str = None,
    config_file: str = 'Project',
    **cmdargs,
) -> CmdResult:
    return set_result(lib.bump_version(**strip_args(locals())))
