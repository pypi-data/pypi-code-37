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


def generate_microcode_templates(
        src_dest, true_flag_bitdef, false_flag_bitdef
        ):
    """
    Generate microcode for all the JUMP_IF_XXX_FLAG instructions.

    Args:
        src_dest (str): Name of the module used for both the source and
            destination.
        true_flag_bitdef (str): Bitdef that represents the state of the
            flags if the condition is true, i.e. the operation should
            jump.
        false_flag_bitdef (str): Bitdef that represents the state of the
            flags if the condition is false, i.e. the operation should
            not jump and just execute the next instruction instead.
    Returns:
        list(DataTemplate): DataTemplates for all the
        JUMP_IF_XXX_FLAG instructions.
    """

    data_templates = []

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(src_dest)

    # DataTemplates for when the condition is true - i.e. it should jump
    control_steps = generate_true_control_steps()
    data_templates.extend(
        assemble_instruction(
            instruction_byte_bitdefs, [true_flag_bitdef], control_steps
        )
    )

    # DataTemplates for when the condition is false - i.e. it should
    # just continue to the next instruction
    control_steps = [
        [
            MODULE_CONTROL["PC"]["COUNT"],
        ]
    ]
    data_templates.extend(
        assemble_instruction(
            instruction_byte_bitdefs, [false_flag_bitdef], control_steps
        )
    )

    return data_templates


def generate_instruction_byte_bitdefs(src_dest):
    """
    Generate bitdefs to specify the instruction byte

    Args:
        src_dest (str): Name of the module used for both the source and
            destination.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    instruction_byte_bitdefs = []

    instruction_byte_bitdefs.append(INSTRUCTION_GROUPS["COPY"])
    instruction_byte_bitdefs.append(SRC_REGISTERS[src_dest])
    instruction_byte_bitdefs.append(DEST_REGISTERS[src_dest])

    return instruction_byte_bitdefs


def generate_true_control_steps():
    """
    Generate control steps to carry out the jump.

    Returns:
        list(list(str)): List of list of bitdefs that specify the
        control steps.
    """

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

    return control_steps


def parse_line(line, src_dest, name):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a JUMP_IF_XXX_FLAG assembly line,
    return an empty list instead.

    Args:
        line (str): Assembly line to be parsed.
        src_dest (str): Name of the module used for both the source and
            destination.
        name (str): Name of the Operation.
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
        generate_instruction_byte_bitdefs(src_dest)
    )

    mc_bytes = []

    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "instruction"
    mc_byte["bitstring"] = instruction_byte
    mc_bytes.append(mc_byte)

    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "constant"
    mc_byte["constant"] = signature[0]["value"]
    mc_bytes.append(mc_byte)

    return mc_bytes


def generate_signatures():
    """
    Generate all the argument signatures for the JUMP_IF_XXX_FLAG
    operation.

    Returns:
        list(list(dict)): All possible signatures, See
        :func:`~.get_arg_def_template` for more information on an
        argument definition dictionary.
    """

    signatures = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = False
    signatures.append([arg_def])

    return signatures
