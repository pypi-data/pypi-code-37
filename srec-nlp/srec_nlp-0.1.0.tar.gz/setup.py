# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['srec_nlp']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-language>=1.2,<2.0', 'ibm-watson>=3.0,<4.0']

setup_kwargs = {
    'name': 'srec-nlp',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Stelios Tymvios',
    'author_email': 'stelios.tymvios@icloud.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
