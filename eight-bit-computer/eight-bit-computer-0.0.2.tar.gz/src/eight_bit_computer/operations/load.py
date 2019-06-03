"""
The LOAD operation.

Loads a value from data memory into a module.
"""

from itertools import product

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


_NAME = "LOAD"


def generate_microcode_templates():
    """
    Generate microcode for all the LOAD instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the LOAD instructions.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_signatures():
    """
    Generate the definitions of all possible arguments passable.

    Returns:
        list(list(dict)): All possible arguments. See
        :func:`~.get_arg_def_template` for more information.
    """

    signatures = []
    sources = ("ACC", "A", "B", "C", "PC", "SP")
    destinations = ("ACC", "A", "B", "C")

    for src, dest in product(sources, destinations):
        signature = []

        arg0_def = get_arg_def_template()
        arg0_def["value_type"] = "module_name"
        arg0_def["is_memory_location"] = True
        arg0_def["value"] = src
        signature.append(arg0_def)

        arg1_def = get_arg_def_template()
        arg1_def["value_type"] = "module_name"
        arg1_def["value"] = dest
        signature.append(arg1_def)

        signatures.append(signature)

    for dest in destinations:
        signature = []

        arg0_def = get_arg_def_template()
        arg0_def["value_type"] = "constant"
        arg0_def["is_memory_location"] = True
        signature.append(arg0_def)

        arg1_def = get_arg_def_template()
        arg1_def["value_type"] = "module_name"
        arg1_def["value"] = dest
        signature.append(arg1_def)

        signatures.append(signature)

    return signatures


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a load with the given args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular load operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define this load.
    """

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)

    flags_bitdefs = [FLAGS["ANY"]]

    control_steps = generate_control_steps(signature)

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs(signature):
    """
    Generate bitdefs to specify the instruction byte for these args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular LOAD operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    if signature[0]["value_type"] == "constant":
        instruction_byte_bitdefs = [
            INSTRUCTION_GROUPS["LOAD"],
            SRC_REGISTERS["CONST"],
            DEST_REGISTERS[signature[1]["value"]],
        ]
    elif signature[0]["value_type"] == "module_name":
        instruction_byte_bitdefs = [
            INSTRUCTION_GROUPS["LOAD"],
            SRC_REGISTERS[signature[0]["value"]],
            DEST_REGISTERS[signature[1]["value"]],
        ]

    return instruction_byte_bitdefs


def generate_control_steps(signature):
    """
    Generate control steps for these args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular load operation to generate the
            control steps for.
    Returns:
        list(list(str)): List of list of bitdefs that specify the
        control steps.
    """
    if signature[0]["value_type"] == "module_name":
        # E.g. LOAD [A] B
        control_steps = [
            [
                MODULE_CONTROL[signature[0]["value"]]["OUT"],
                MODULE_CONTROL["MAR"]["IN"],
            ],
            [
                MODULE_CONTROL["RAM"]["SEL_DATA_MEM"],
                MODULE_CONTROL["RAM"]["OUT"],
                MODULE_CONTROL[signature[1]["value"]]["IN"],
            ],
        ]
    elif signature[0]["value_type"] == "constant":
        # E.g. LOAD [$var] ACC
        control_steps = [
            [
                MODULE_CONTROL["PC"]["OUT"],
                MODULE_CONTROL["MAR"]["IN"],
            ],
            [
                MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
                MODULE_CONTROL["RAM"]["OUT"],
                MODULE_CONTROL["MAR"]["IN"],
                MODULE_CONTROL["PC"]["COUNT"],
            ],
            [
                MODULE_CONTROL["RAM"]["SEL_DATA_MEM"],
                MODULE_CONTROL["RAM"]["OUT"],
                MODULE_CONTROL[signature[1]["value"]]["IN"],
            ],
        ]

    return control_steps


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a LOAD assembly line, return an empty
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

    if signature[0]["value_type"] == "constant":
        mc_byte = get_machine_code_byte_template()
        mc_byte["byte_type"] = "constant"
        mc_byte["constant"] = signature[0]["value"]
        mc_bytes.append(mc_byte)

    return mc_bytes
