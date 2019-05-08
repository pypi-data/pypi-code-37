import sys
import os
import click
import logging
from mcutk import __version__


LEVELS = {
    'warning': logging.WARNING,
    'debug': logging.DEBUG,
    'info': logging.INFO
}



class ComplexCLI(click.MultiCommand):

    COMMANDS = [
        'build',
        'scan',
        'config',
        # 'gdbserver',
        'flash'
    ]

    def list_commands(self, ctx):
        return self.COMMANDS


    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('mcutk.commands.' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli



@click.command(cls=ComplexCLI, invoke_without_command=True, help="mcutk command line tool")
@click.option('--version', is_flag=True, help="show mcutk version")
@click.option('-D', '--DEBUG', default=False, is_flag=True, help='enable debug logging level')
def main(version=False, debug=False):
    if debug:
        level = LEVELS.get('debug', logging.WARNING)
        logging.basicConfig(level=level)

    if version:
        click.echo(__version__)



if __name__ == '__main__':
    main()
