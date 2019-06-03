"""
Base for simple ALU operations
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    MODULE_CONTROL,
    ALU_OPERANDS,
    ALU_OPERATIONS,
    ALU_CONTROL_FLAGS,
    FLAGS,
    instruction_byte_from_bitdefs,
)
from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)


def generate_microcode_templates(alu_op, control_flags):
    """
    Generate microcode for all the ADD instructions.

    Args:
        alu_op (str): The ALU operation to perform - one of the
            ALU_OPERATIONS.
        control_flags (list(str)): List of ALU control flags for this
            ALU operation. One of the ALU_CONTROL_FLAGS.
    Returns:
        list(DataTemplate): DataTemplates for all the ADD instructions.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(
            signature, alu_op, control_flags
        )
        data_templates.extend(templates)

    return data_templates


def generate_signatures():
    """
    Generate all the argument signatures for the ADD operation.

    Returns:
        list(list(dict)): All possible signatures, See
        :func:`~.get_arg_def_template` for more information on an
        argument definition dictionary.
    """

    signatures = []
    alu_args = ("A", "B", "C")
    for alu_arg in alu_args:
        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["is_memory_location"] = False
        arg_def["value"] = alu_arg
        signatures.append([arg_def])

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = False
    signatures.append([arg_def])

    return signatures


def generate_operation_templates(signature, alu_op, control_flags):
    """
    Create the DataTemplates to define a ADD with the given signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular ADD operation to generate
            templates for.
        alu_op (str): The ALU operation to perform - one of the
            ALU_OPERATIONS.
        control_flags (list(str)): List of ALU control flags for this
            ALU operation. One of the ALU_CONTROL_FLAGS.
    Returns:
        list(DataTemplate) : DataTemplates that define this ADD.
    """

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(
        signature, alu_op
    )

    flags_bitdefs = [FLAGS["ANY"]]

    control_steps = generate_control_steps(signature, control_flags)

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs(signature, alu_op):
    """
    Generate bitdefs to specify the instruction byte for this signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular ADD operation to generate
            the instruction byte bitdefs for.
        alu_op (str): The ALU operation to perform - one of the
            ALU_OPERATIONS.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    if signature[0]["value_type"] == "module_name":
        bitdefs = [
            INSTRUCTION_GROUPS["ALU"],
            alu_op,
            ALU_OPERANDS[signature[0]["value"]],
        ]
    elif signature[0]["value_type"] == "constant":
        bitdefs = [
            INSTRUCTION_GROUPS["ALU"],
            alu_op,
            ALU_OPERANDS["ACC/CONST"],
        ]

    return bitdefs


def generate_control_steps(signature, control_flags):
    """
    Generate control steps for this signature.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular ADD operation to generate the
            control steps for.
        control_flags (list(str)): List of ALU control flags for this
            ALU operation. One of the ALU_CONTROL_FLAGS.
    Returns:
        list(list(str)): List of list of bitdefs that specify the
        control steps.
    """

    if signature[0]["value_type"] == "module_name":
        step_0 = [
            MODULE_CONTROL[signature[0]["value"]]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        step_0.extend(control_flags)

        step_1 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1]

    elif signature[0]["value_type"] == "constant":
        step_0 = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        step_1 = [
            MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
            MODULE_CONTROL["RAM"]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        step_1.extend(control_flags)

        step_2 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1, step_2]

    return control_steps


def parse_line(line, name, alu_op):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a ADD assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
        name (str): Name of the Operation.
        alu_op (str): The ALU operation to perform - one of the
            ALU_OPERATIONS.
    Returns:
        list(dict): List of machine code byte template dictionaries or
        an empty list.
    """

    match, signature = match_and_parse_line(
        line, name, generate_signatures()
    )

    if not match:
        return []

    instruction_byte = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs(signature, alu_op)
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
