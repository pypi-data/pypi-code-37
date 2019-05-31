# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['foxcross']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.4.0,<0.5.0',
 'jinja2>=2.10,<3.0',
 'python-slugify>=3.0,<4.0',
 'starlette>=0.12.0,<0.13.0',
 'unidecode>=1.0,<2.0',
 'uvicorn>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'foxcross',
    'version': '0.1.0',
    'description': 'Asyncio serving for data science models',
    'long_description': None,
    'author': 'Steven Pate',
    'author_email': 'steven@laac.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
