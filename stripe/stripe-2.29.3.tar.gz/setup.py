# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['stripe',
 'stripe.api_resources',
 'stripe.api_resources.abstract',
 'stripe.api_resources.checkout',
 'stripe.api_resources.issuing',
 'stripe.api_resources.radar',
 'stripe.api_resources.reporting',
 'stripe.api_resources.sigma',
 'stripe.api_resources.terminal']

package_data = \
{'': ['*'], 'stripe': ['data/*']}

install_requires = \
['toml>=0.9,<0.10']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['requests[security]>=2.20,<3.0'],
 ':python_version >= "3.4" and python_version < "4.0"': ['requests>=2.20,<3.0']}

setup_kwargs = {
    'name': 'stripe',
    'version': '2.29.3',
    'description': 'Python bindings for the Stripe API',
    'long_description': "Official Stripe Bindings for Python\n===================================\n\nA Python library for Stripe's API.\n\n\nSetup\n-----\n\nYou can install this package by using the pip tool and installing:\n\n    $ pip install stripe\n    \nOr:\n\n    $ easy_install stripe\n    \n\nSetting up a Stripe Account\n---------------------------\n\nSign up for Stripe at https://dashboard.stripe.com/register.\n\nUsing the Stripe API\n--------------------\n\nDocumentation for the python bindings can be found alongside Stripe's other bindings here:\n\n- https://stripe.com/docs\n- https://stripe.com/docs/api/python\n\nIn the standard documentation (the first link), most of the reference pages will have examples in Stripe's official bindings (including Python). Just click on the Python tab to get the relevant documentation.\n\nIn the full API reference for python (the second link), the right half of the page will provide example requests and responses for various API calls.\n",
    'author': 'Stripe',
    'author_email': 'support@stripe.com',
    'url': 'https://github.com/stripe/stripe-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
