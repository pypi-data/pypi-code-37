"""
Top level interface for the module
"""

import os

from .assembler import process_assembly_lines
from .assembly_summary import generate_assembly_summary
from .exceptions import AssemblyError
from . import export
from . import rom


def assemble(
        input_filepath,
        output_filepath=None,
        variable_start_offset=0,
        output_format="logisim",
        ):
    """
    Read an assembly file and write out equivalent machine code.

    Args:
        input_filepath (str): The location of the assembly file.
        output_filepath (str) (optional): The location to write out the
            machine code. If nothing is passed, the output path will be
            the input path with the extension changed to mc.
        variable_start_offset (int) (optional): How far to offset the
            first variable in data memory from 0.
        output_format (str) (optional): How to format the output.
            ``logisim`` or ``cpp``.
    """

    # Does input file exist
    if not os.path.isfile(input_filepath):
        print "Input file: {input_filepath} does not exist.".format(
            input_filepath=input_filepath)
        return

    # Does input file have the correct extension
    if not input_filepath.endswith(".asm"):
        print "Input file must have a .asm extension."
        return

    # Validate/generate output filepath
    if output_filepath is None:
        output_filepath = get_mc_filepath(input_filepath)
    output_dir = os.path.dirname(output_filepath)
    if output_dir == "":
        output_filepath = "./{output_filepath}".format(
            output_filepath=output_filepath
        )
    elif not os.path.isdir(output_dir):
        print "Output directory: {output_dir} does not exist.".format(
            output_dir=output_dir
        )
        return

    # Do assembly
    lines = filepath_to_lines(input_filepath)
    try:
        assembly_line_infos = process_assembly_lines(
            lines, variable_start_offset=variable_start_offset
        )
    except AssemblyError as inst:
        print inst.args[0]
        return

    # Success message and summary
    completion_msg = (
        "Assembly complete. Assembly file written to: {output_filepath}."
        "\n\nAssembly summary:\n".format(output_filepath=output_filepath)
    )
    print completion_msg
    print generate_assembly_summary(assembly_line_infos)

    # Convert to correct format
    mc_byte_bitstrings = extract_machine_code(assembly_line_infos)
    if output_format == "logisim":
        output = export.bitstrings_to_logisim(mc_byte_bitstrings)
    elif output_format == "cpp":
        output = export.bitstrings_to_cpp(mc_byte_bitstrings)

    # Write file.
    with open(output_filepath, "w") as file:
        file.write(output)


def filepath_to_lines(input_filepath):
    """
    Take a filepath and get all the lines of the file.

    The lines returned have the newline stripped.

    Args:
        input_filepath (str): Path to the file of disk to read.
    Returns:
        list(str): Lines of the file.
    """
    with open(input_filepath) as file:
        lines = file.read().splitlines()
    return lines


def get_mc_filepath(asm_path):
    """
    Get the filepath for the machine code.

    This is the assembly filepath with .asm replaced with .mc

    Args:
        asm_path (str): Path to the assembly file.
    Returns:
        str: Path to the machine code file.
    """

    return "{basepath}.mc".format(basepath=asm_path[:-4])


def extract_machine_code(assembly_lines):
    """
    Extract machine code from assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly line info
            dictionaries to extract machine code from. See
            :func:`~.get_assembly_line_template` for details on what
            those dictionaries contain.
    Returns:
        list(str): List of bit strings for the machine code.
    """
    machine_code = []
    for assembly_line in assembly_lines:
        if assembly_line["has_machine_code"]:
            for mc_byte in assembly_line["mc_bytes"]:
                machine_code.append(mc_byte["bitstring"])
    return machine_code


def gen_roms(output_dir=".", rom_prefix="rom", output_format="logisim"):
    """
    Write files containing microcode for drive the roms.

    Args:
        output_dir (str) (optional): The directory to write the roms
            into.
        rom_prefix (str) (optional): The prefix for the rom files.
        output_format (str) (optional): How to foramt the output.
            ``logisim`` or ``cpp``.
    """

    if not os.path.isdir(output_dir):
        print "Output directory: {output_dir} does not exist.".format(
            output_dir=output_dir
        )
        return

    rom_data = rom.get_rom()
    rom_slices = rom.slice_rom(rom_data)
    for rom_index, rom_slice in rom_slices.iteritems():
        slice_bitstrings = [romdata.data for romdata in rom_slice]
        if output_format == "logisim":
            output = export.bitstrings_to_logisim(slice_bitstrings)
        elif output_format == "cpp":
            output = export.bitstrings_to_cpp(slice_bitstrings)

        rom_filename = "{rom_prefix}_{rom_index}".format(
            rom_prefix=rom_prefix, rom_index=rom_index
        )
        filepath = os.path.join(output_dir, rom_filename)

        with open(filepath, "w") as romfile:
            romfile.write(output)

    msg = "ROM writing complete. ROMs written to {output_dir}".format(
        output_dir=output_dir
    )
    print msg
