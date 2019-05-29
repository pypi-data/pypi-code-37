# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['rarbg']
install_requires = \
['aiohttp>=3.5,<4.0',
 'click>=7.0,<8.0',
 'humanize>=0.5.1,<0.6.0',
 'jinja2>=2.10,<3.0',
 'python-dateutil>=2.8,<3.0']

entry_points = \
{'console_scripts': ['rarbg = rarbg:main']}

setup_kwargs = {
    'name': 'rarbg',
    'version': '1.2.0',
    'description': 'RSS interface to TorrentAPI',
    'long_description': None,
    'author': 'banteg',
    'author_email': 'banteeg@gmail.com',
    'url': 'https://github.com/banteg/rarbg',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
