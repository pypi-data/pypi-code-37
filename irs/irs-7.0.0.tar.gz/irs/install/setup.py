import errno
import os
import sys

import ydl_binaries

from .config_file import CONF_FILE


def set_it_up():
    """Sets up the config folder and files for the irs program"""
    conf_path = os.environ.get("irs_config_dir") \
        or os.environ["HOME"] + "/.irs"
    bin_path = os.path.join(conf_path, "bin")

    make_if_not_exist(conf_path)
    make_if_not_exist(bin_path)

    ydl_binaries.download_ffmpeg(bin_path)

    if not os.path.isfile(os.path.join(conf_path, "config.yml")):
        with open(os.path.join(conf_path, "config.yml"), "w") as config:
            config.write(CONF_FILE)

    print("\nYour config folder:")
    print(conf_path + "/")
    print("  config.yml \t# For editing spotify keys and default music directory")
    print("  bin/       \t# Binary folder for MP3 extraction")
    print("    ffmpeg")
    print("    ffprobe")

    sys.exit(0)


def make_if_not_exist(path):
    """Checks if a path exists and if it doesn't, it makes it
    :param path: a string, the path to check
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise