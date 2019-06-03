"""
Template for operation module
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
    instruction_byte_from_bitdefs,
)
from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "OP_TEMPLATE"


def generate_microcode_templates():
    """
    Generate microcode for all the OP_TEMPLATE instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the OP_TEMPLATE instructions.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_signatures():
    """
    Generate all the argument signatures for the OP_TEMPLATE operation.

    Returns:
        list(list(dict)): All possible signatures, See
        :func:`~.get_arg_def_template` for more information on an
        argument definition dictionary.
    """

    pass


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a OP_TEMPLATE with the given signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular OP_TEMPLATE operation to generate
            templates for.
    Returns:
        list(DataTemplate) : DataTemplates that define this OP_TEMPLATE.
    """

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)

    flags_bitdefs = [FLAGS["ANY"]]

    control_steps = generate_control_steps(signature)

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs(signature):
    """
    Generate bitdefs to specify the instruction byte for this signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular OP_TEMPLATE operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    pass


def generate_control_steps(signature):
    """
    Generate control steps for this signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular OP_TEMPLATE operation to generate the
            control steps for.
    Returns:
        list(list(str)): List of list of bitdefs that specify the
        control steps.
    """

    pass


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a OP_TEMPLATE assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of machine code byte template dictionaries or
        an empty list.
    """

    match, signature = match_and_parse_line(
        line, _NAME, generate_signatures()
    )

    if not match:
        return []

    instruction_byte = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs(signature)
    )

    mc_bytes = []

    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "instruction"
    mc_byte["bitstring"] = instruction_byte
    mc_bytes.append(mc_byte)

    return mc_bytes
