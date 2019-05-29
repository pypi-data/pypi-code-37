import os
import angreal

from angreal.integrations.virtual_env import VirtualEnv
from angreal import win,error
import click

HERE = os.path.dirname(__file__)
HOME = os.path.expanduser("~")
REQUIREMENTS = os.path.realpath(os.path.join(HERE,'..','requirements','requirements.txt'))
DEV_REQUIREMENTS = os.path.realpath(os.path.join(HERE,'..','requirements','dev.txt'))


@angreal.command()
@angreal.option('--dev',is_flag=True, help='Set up the development environment')
def angreal_cmd(dev):
    """
    update or create the virtual environment
    """
    requirements = REQUIREMENTS

    if dev:
        requirements = DEV_REQUIREMENTS

    if not os.path.isfile(requirements):
        error('{} , does not exist'.format(requirements))

    try:
        venv = VirtualEnv(name='module_name', python='python3',requirements=requirements)
        win('Virtual environment setup successful.'))
    except Exception as e:
        error('Virtual environment failed with : \n {}'.format(e))



    return