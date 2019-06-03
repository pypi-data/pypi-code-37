"""
ADD Operation
"""

from . import simple_alu_op_base

from ..language_defs import (
    ALU_OPERATIONS,
    ALU_CONTROL_FLAGS,
    instruction_byte_from_bitdefs,
)

_NAME = "ADD"


def generate_microcode_templates():
    """
    Generate microcode for all the ADD instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the ADD instructions.
    """

    return simple_alu_op_base.generate_microcode_templates(
        ALU_OPERATIONS["ADD"],
        ALU_CONTROL_FLAGS["A_PLUS_B"],
    )


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a ADD assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of machine code byte template dictionaries or
        an empty list.
    """

    return simple_alu_op_base.parse_line(
        line, _NAME, ALU_OPERATIONS["ADD"]
    )
