import os
import sys
import importlib
here = os.path.dirname(__file__)

sys.path.append(os.path.abspath(
        os.path.join(here,'..','..','..','project','{{ cookiecutter.name }}')
        ),
        os.path.join(os.path.expanduser('~'),'.venv','{{ cookiecutter.name }}')
        )

import {{ cookiecutter.name }}


def refresh():
    """
    refreshes the module so code in the library can be tested without a kernel restart

    :return:
    """
    importlib.reload({{ cookiecutter.name }})