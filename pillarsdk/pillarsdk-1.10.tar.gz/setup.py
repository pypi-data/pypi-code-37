# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pillarsdk']

package_data = \
{'': ['*']}

install_requires = \
['pyOpenSSL>=19,<20', 'requests>=2,<3']

setup_kwargs = {
    'name': 'pillarsdk',
    'version': '1.10',
    'description': 'The Pillar REST SDK provides Python APIs to communicate to the Pillar webservices.',
    'long_description': None,
    'author': 'Francesco Siddi',
    'author_email': 'francesco@blender.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
