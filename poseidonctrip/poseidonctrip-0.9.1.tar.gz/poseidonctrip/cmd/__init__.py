"""
Usage:
  poseidonctrip init [--folder=<folder>]
  poseidonctrip migrate
  poseidonctrip createsuperuser
  poseidonctrip runserver [<host:port>]

Options:
  -h --help
  -v --version
"""

from docopt import docopt
from poseidonctrip import version
from poseidonctrip.cmd.init import init
from poseidonctrip.cmd.server import server


def cmd():
    arguments = docopt(__doc__, version=version())
    
    if arguments.get('init'):
        # nit folder
        init(arguments.get('--folder'))
    else:
        # Call django cmd
        server()
