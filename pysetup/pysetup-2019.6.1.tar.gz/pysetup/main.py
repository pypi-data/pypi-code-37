from .command import Command
import sys


def main():
    return Command.execute(*sys.argv[1:])
