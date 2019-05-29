# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['spider_domainauth', 'spider_domainauth.migrations']

package_data = \
{'': ['*']}

install_requires = \
['spkcspider>=0.8a2']

setup_kwargs = {
    'name': 'spkcspider-domainauth',
    'version': '0.1.2',
    'description': 'Helper for spkcspiders domain authentication',
    'long_description': '\n\nHelper for db based domain auth\n\n# Installation\n\n~~~~ sh\npip install spider-domainauth\n~~~~\n\nsettings:\n\n~~~~\n...\nINSTALLED_APPS = [\n...\n    spider_domainauth\n...\n]\n~~~~\n\n# Usage:\n\n~~~~ python\nfrom spider_domainauth.models import ReverseToken\n\n# overloaded method\nReverseToken.object.create(secret="kskls")\n~~~~\n\n\n# TODO:\n* overload other manager methods\n* better examples\n',
    'author': 'Alexander Kaftan',
    'author_email': None,
    'url': 'https://github.com/spkcspider/spkcspider-domainauth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
