# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['announcer']

package_data = \
{'': ['*']}

install_requires = \
['mistletoe>=0.7.1,<0.8.0', 'requests>=2.19,<3.0', 'typing>=3.6.4,<4.0.0']

entry_points = \
{'console_scripts': ['announce = announcer.__init__:main']}

setup_kwargs = {
    'name': 'announcer',
    'version': '2.1.0',
    'description': 'Announce changes in keepachangelog-style CHANGELOG.md files to Slack',
    'long_description': '# announcer\n\nThis tool:\n* takes an [keepachangelog](https://keepachangelog.com/en/1.0.0/)-style CHANGELOG.md file\n* extracts all changes for a particular version\n* and sends a formatted message to a Slack webhook. \n\n## Installation\n\nInstall this tool using pip:\n\n```\npip install announcer\n```\n\n## Tool usage\n\n```\nusage: announce [-h] --slackhook SLACKHOOK --changelogversion CHANGELOGVERSION\n                --changelogfile CHANGELOGFILE --projectname PROJECTNAME\n                [--username USERNAME]\n                [--iconurl ICONURL | --iconemoji ICONEMOJI]\n\nAnnounce CHANGELOG changes on Slack\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --slackhook SLACKHOOK\n                        The incoming webhook URL\n  --changelogversion CHANGELOGVERSION\n                        The changelog version to announce (e.g. 1.0.0)\n  --changelogfile CHANGELOGFILE\n                        The file containing changelog details (e.g.\n                        CHANGELOG.md)\n  --projectname PROJECTNAME\n                        The name of the project to announce (e.g. announcer)\n  --username USERNAME   The username that the announcement will be made as\n                        (e.g. qs-announcer)\n  --iconurl ICONURL     A URL to use for the user icon in the announcement\n  --iconemoji ICONEMOJI\n                        A Slack emoji code to use for the user icon in the\n                        announcement (e.g. party_parrot)\n```\n',
    'author': 'Max Dymond',
    'author_email': 'max.dymond@metaswitch.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
