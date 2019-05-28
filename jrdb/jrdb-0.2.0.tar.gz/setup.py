# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jrdb', 'jrdb.schema']

package_data = \
{'': ['*'], 'jrdb': ['data/*']}

install_requires = \
['fastavro>=0.21.18,<0.22.0',
 'google-cloud-storage>=1.13,<2.0',
 'lxml>=4.3,<5.0',
 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'jrdb',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'otomarukanta',
    'author_email': 'kanta208@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
