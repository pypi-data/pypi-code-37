import argparse

from . import main


def assemble():
    """
    Entry point for the command line assemble script.
    """
    parser = get_assemble_parser()
    args = parser.parse_args()
    main.assemble(
        args.asm_filepath,
        output_filepath=args.output_filepath,
        variable_start_offset=args.variable_start_offset,
        output_format=args.output_format,
    )


def get_assemble_parser():
    """
    Generate arg parser for the ebc_assemble command line script.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Assemble eight bit computer assembly files to machine "
            "code."
        )
    )
    parser.add_argument(
        "asm_filepath", help="Path to the assembly file to assemble."
    )
    parser.add_argument(
        "-o",
        "--output_filepath",
        help=(
            "Filepath to write the machine code to. E.g. "
            "\"../machine_code.mc\". Including ./ for a file in the "
            "current directory is optional."
        )
    )
    parser.add_argument(
        "-s",
        "--variable_start_offset",
        type=positive_int,
        help=(
            "Index in data memory to start assigning automatically "
            "assigned variables at."
        ),
        default=0,
    )
    parser.add_argument(
        "-f",
        "--output_format",
        choices=["logisim", "cpp"],
        help="Format to write the machine code in.",
        default="logisim",
    )

    return parser


def positive_int(value):
    """
    Validate a string is an int greater than or equal to zero.

    Used for the type argument in an
    argparse.ArgumentParser.add_argument call.

    Args:
        value (str): Value to be tested.
    Returns:
        int: Value as an integer if it was >= 0.
    Raises:
        argparse.ArgumentTypeError: If the value was not greater than or
            equal to zero.
    """
    error_template = "{value} is not an integer greater than or equal to 0."

    # Check if it's an int.
    try:
        int_val = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(error_template.format(value=value))

    # Check if it's a positive int.
    if int_val < 0:
        raise argparse.ArgumentTypeError(error_template.format(value=value))

    return int_val


def gen_roms():
    """
    Entry point for the command line rom generation script.
    """
    parser = get_gen_roms_parser()
    args = parser.parse_args()
    main.gen_roms(
        output_dir=args.output_dir,
        rom_prefix=args.rom_prefix,
        output_format=args.output_format,
    )


def get_gen_roms_parser():
    """
    Generate arg parser for the gen_roms command line script.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Generate ROMs that contain the microcode."
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Directory to write the ROMs into.",
        default=".",
    )
    parser.add_argument(
        "-p",
        "--rom_prefix",
        help="Prefix for the ROM files.",
        default="rom",
    )
    parser.add_argument(
        "-f",
        "--output_format",
        choices=["logisim", "cpp"],
        help="Format to write the ROMs in.",
        default="logisim",
    )

    return parser