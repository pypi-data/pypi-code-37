from .command import Command
import sys


def main():
    cmd = sys.argv[1]
    params = sys.argv[2:]
    host = 'localhost'
    port = 6991
    for i, param in enumerate(params):
        if param in ['-h', '-p']:
            if param == '-h': host = params[i + 1]
            else: port = int(params[i + 1])
            del params[i + 1]
    return Command.execute(cmd, *params, host=host, port=port)
