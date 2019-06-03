"""
JUMP Operation
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

_NAME = "JUMP"


def generate_microcode_templates():
    """
    Generate microcode for all the JUMP instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP instructions.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_signatures():
    """
    Generate all the argument signatures for the jump operation.

    Returns:
        list(list(dict)): All possible signatures, See
        :func:`~.get_arg_def_template` for more information on an
        argument definition dictionary.
    """

    signatures = []
    direct_modules = ("ACC", "A", "B", "C", "SP")
    memory_refs = ("ACC", "A", "B", "C", "PC", "SP")

    for module in direct_modules:
        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["is_memory_location"] = False
        arg_def["value"] = module
        signatures.append([arg_def])

    for module in memory_refs:
        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["is_memory_location"] = True
        arg_def["value"] = module
        signatures.append([arg_def])

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = False
    signatures.append([arg_def])

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = True
    signatures.append([arg_def])

    return signatures


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a JUMP with the given signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular JUMP operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define this JUMP.
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
            specify which particular JUMP operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    instruction_byte_bitdefs = []

    instruction_byte_bitdefs.append(DEST_REGISTERS["PC"])
    if signature[0]["is_memory_location"]:
        instruction_byte_bitdefs.append(INSTRUCTION_GROUPS["LOAD"])
    else:
        instruction_byte_bitdefs.append(INSTRUCTION_GROUPS["COPY"])

    if signature[0]["value_type"] == "constant":
        instruction_byte_bitdefs.append(SRC_REGISTERS["CONST"])
    elif signature[0]["value_type"] == "module_name":
        instruction_byte_bitdefs.append(SRC_REGISTERS[signature[0]["value"]])

    return instruction_byte_bitdefs


def generate_control_steps(signature):
    """
    Generate control steps for this signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular JUMP operation to generate the
            control steps for.
    Returns:
        list(list(str)): List of list of bitdefs that specify the
        control steps.
    """

    if signature[0]["is_memory_location"]:
        if signature[0]["value_type"] == "constant":
            # E.g. JUMP [$var]
            control_steps = [
                [
                    MODULE_CONTROL["PC"]["OUT"],
                    MODULE_CONTROL["MAR"]["IN"],
                ],
                [
                    MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
                    MODULE_CONTROL["RAM"]["OUT"],
                    MODULE_CONTROL["MAR"]["IN"],
                ],
                [
                    MODULE_CONTROL["RAM"]["SEL_DATA_MEM"],
                    MODULE_CONTROL["RAM"]["OUT"],
                    MODULE_CONTROL["PC"]["IN"],
                ],
            ]
        if signature[0]["value_type"] == "module_name":
            # E.g. JUMP [A]
            control_steps = [
                [
                    MODULE_CONTROL[signature[0]["value"]]["OUT"],
                    MODULE_CONTROL["MAR"]["IN"],
                ],
                [
                    MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
                    MODULE_CONTROL["RAM"]["OUT"],
                    MODULE_CONTROL["MAR"]["IN"],
                ],
                [
                    MODULE_CONTROL["RAM"]["SEL_DATA_MEM"],
                    MODULE_CONTROL["RAM"]["OUT"],
                    MODULE_CONTROL["PC"]["IN"],
                ],
            ]
    else:
        if signature[0]["value_type"] == "constant":
            # E.g. JUMP @label
            control_steps = [
                [
                    MODULE_CONTROL["PC"]["OUT"],
                    MODULE_CONTROL["MAR"]["IN"],
                ],
                [
                    MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
                    MODULE_CONTROL["RAM"]["OUT"],
                    MODULE_CONTROL["PC"]["IN"],
                ],
            ]
        if signature[0]["value_type"] == "module_name":
            # E.g. JUMP A
            control_steps = [
                [
                    MODULE_CONTROL[signature[0]["value"]]["OUT"],
                    MODULE_CONTROL["PC"]["IN"],
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