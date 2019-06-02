import sys


def error(message):
    print("ERROR: {}".format(message), file=sys.stderr)
    return None
