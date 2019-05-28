#!/usr/bin/env python3
""""""

import argparse
import os
import sys

import python_releaser


def main():
    parser = argparse.ArgumentParser(
        description='pyreleaser: sane release flow for python projects',
    )
    parser.add_argument(
        '--version', required=False, action='store_true',
        help='print the version',
    )

    args = parser.parse_args()

    if args.version:
        os.write(sys.stdout, python_releaser.__version__ + '\n')
        return

    print('not yet implemented')


if __name__ == '__main__':
    main()
