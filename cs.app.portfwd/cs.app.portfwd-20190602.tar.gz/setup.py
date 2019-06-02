#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.app.portfwd',
  description = 'Manage persistent ssh tunnels and port forwards.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190602',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  entry_points = {'console_scripts': ['portfwd = cs.app.portfwd:main']},
  include_package_data = True,
  install_requires = ['cs.app.flag', 'cs.app.svcd', 'cs.env', 'cs.logutils', 'cs.pfx', 'cs.psutils', 'cs.py.func', 'cs.sh'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 (GPLv3)',
  long_description = 'Manage persistent ssh tunnels and port forwards.\n\nPortfwd runs a collection of ssh tunnel commands persistently,\neach in its own `cs.app.svcd <https://pypi.org/project/cs.app.svcd>`_ instance\nwith all the visibility and process control that SvcD brings.\n\nIt reads tunnel preconditions from special comments within the ssh config file.\nIt uses the configuration options from the config file\nas the SvcD signature function\nthus restarting particular ssh tunnels when their specific configuration changes.\nIt has an "automatic" mode (the -A option)\nwhich monitors the desired list of tunnels\nfrom statuses expressed via `cs.app.flag <https://pypi.org/project/cs.app.flag>`_\nwhich allows live addition or removal of tunnels as needed.\n\n## Function `Condition(portfwd, op, invert, *args)`\n\nFactory to construct a condition from a specification.\n\n## Class `FlagCondition`\n\nMRO: `_PortfwdCondition`  \nA flag based condition.\n\n## Function `main(argv=None, environ=None)`\n\nCommand line main programme.\n\n## Class `PingCondition`\n\nMRO: `_PortfwdCondition`  \nA ping based condition.\n\n## Class `Portfwd`\n\nMRO: `cs.app.flag.FlaggedMixin`  \nAn ssh tunnel built on a SvcD.\n\n### Method `Portfwd.__init__(self, target, ssh_config=None, conditions=(), test_shcmd=None, trace=False, verbose=False, flags=None)`\n\nInitialise the Portfwd.\n\nParameters:\n* `target`: the tunnel name, and also the name of the ssh configuration used\n* `ssh_config`: ssh configuration file if not the default\n* `conditions`: an iterable of `Condition`s\n  which must hold before the tunnel is set up;\n  the tunnel also aborts if these cease to hold\n* `test_shcmd`: a shell command which must succeed\n  before the tunnel is set up;\n  the tunnel also aborts if this command subsequently fails\n* `trace`: issue tracing messages; default `False`\n* `verbose`: be verbose; default `False`\n* `flags`: optional preexisting `Flags` instance\n\n## Class `Portfwds`\n\nA collection of Portfwd instances and associated control methods.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.portfwd'],
)
