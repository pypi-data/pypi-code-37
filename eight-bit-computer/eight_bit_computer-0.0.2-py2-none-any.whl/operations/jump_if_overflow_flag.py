"""
JUMP_IF_OVERFLOW_FLAG operation
"""

from . import jump_if_flag_base
from ..language_defs import FLAGS

_NAME = "JUMP_IF_OVERFLOW_FLAG"


def generate_microcode_templates():
    """
    Generate microcode for all the JUMP_IF_OVERFLOW_FLAG instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the
        JUMP_IF_OVERFLOW_FLAG instructions.
    """

    return jump_if_flag_base.generate_microcode_templates(
        "SP",
        FLAGS["CARRY_BORROW"]["HIGH"],
        FLAGS["CARRY_BORROW"]["LOW"],
    )


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a JUMP_IF_OVERFLOW_FLAG assembly line,
    return an empty list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of machine code byte template dictionaries or
        an empty list.
    """

    return jump_if_flag_base.parse_line(line, "SP", _NAME)
