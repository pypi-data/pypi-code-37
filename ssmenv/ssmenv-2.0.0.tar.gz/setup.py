# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ssmenv']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0']

setup_kwargs = {
    'name': 'ssmenv',
    'version': '2.0.0',
    'description': 'Allows you to read parameters from AWS Parameter Store and operate on results as on dictionary.',
    'long_description': 'SSMEnv\n---\n| master  | coverage | PyPI | Python | Licence |\n| --- | --- | --- | --- | --- |\n| [![Build Status](https://travis-ci.org/whisller/ssmenv.svg?branch=master)](https://travis-ci.org/whisller/ssmenv) | [![Coverage Status](https://coveralls.io/repos/github/whisller/ssmenv/badge.svg?branch=develop)](https://coveralls.io/github/whisller/ssmenv?branch=develop) | [![PyPI](https://img.shields.io/pypi/v/ssmenv.svg)](https://pypi.org/project/ssmenv/) | ![](https://img.shields.io/pypi/pyversions/ssmenv.svg) | ![](https://img.shields.io/pypi/l/ssmenv.svg) |\n\n---\nSSMEnv allows you to read parameters from [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html) and operate on results as on dictionary.\n\n## Installation\nOnly requirement is to have `boto3` installed.\n```bash\npip install ssmenv\n```\n\n## Reading parameters\nLet\'s assume we have two parameters `token` and `url` under `/service/my-service` namespace.\nReading both parameters is as simple as initialising class object.\n```python\nfrom ssmenv import SSMEnv\n\nparams = SSMEnv("/service/my-service")\n```\n\nDone! Now we can access `/service/my-service/token` and `/service/my-service/url` in `params` variable!\n\nNow `params` can be accesses as python `dict` type.\n\n## Interacting with `SSMEnv` instance\nAs you know by now, instance of `SSMEnv` can be accessed as any `dict` in python which means you can do things like:\n```python\nfrom ssmenv import SSMEnv\n\nparams = SSMEnv("/service/my-service")\n\n# 1. Access value directly\ntoken = params["SERVICE_MY_SERVICE_TOKEN"]\n\n# 2. Get list of all loaded parameter\'s names\nlist(params.keys())\n\n# 3. Get list of all loaded parameter\'s values\nlist(params.values())\n\n# and so on...\n```\n\n## Fetching multiple namespaces at once\nIn real world most often you will access parameters from different namespaces, you can easily do that with `SSMEnv`\nby passing `tuple`\n```python\nfrom ssmenv import SSMEnv\n\nparams = SSMEnv("/service/my-service", "/resource/mysql")\n```\nNow `params` will have all parameters from both `/service/my-service` and `/resource/mysql`.\n\n## AWS Lambda decorator\nIf you use AWS lambda, you might find handy `ssmenv` decorator. It behaves same as if you would initialise `SSMEnv` by hand, but additionally it injects instance of `SSMEnv` into `context.params` attribute.\n\n```python\nfrom ssmenv import ssmenv\n\n@ssmenv("/service/my-service")\ndef handler(event, context):\n    return context.params\n```\n\n## Populating `os.environ`\nYou can hide use of `SSMEnv` by using `os.environ` dict.\n```python\nimport os\nfrom ssmenv import SSMEnv\n\nos.environ = {**os.environ, **SSMEnv("/service/my-service")}\n```\n\n## Removing common prefixes\nAccessing your parameters through whole namespaces can sometimes be not convenient\nespecially if you have very long names.\n\nHence why you can use `prefixes` parameter, to make your code cleaner.\n\n ```python\nfrom ssmenv import SSMEnv\n\nparams = SSMEnv("/service/my-service", prefixes=("/service/my-service",))\nparams["TOKEN"]\n```\n\n## Returning dict in case there is no AWS context\nYou might want to run your application without AWS, e.g. through docker on your local machine and mock parameters.\nFor that you can use `no_aws_default` attribute.\n\n```python\nimport os\nfrom ssmenv import SSMEnv\n\nos.environ["SERVICE_MY_SERVICE_TOKEN"] = "mocked-token" # that might be set in docker-compose\n\nparams = SSMEnv("/service/my-service", no_aws_default=os.environ)\n```\n\n## Passing your own boto3 client\nYou can pass your own boto3 client as well.\n```python\nimport boto3\nfrom ssmenv import SSMEnv\n\nssm_client = boto3.client("ssm")\nparams = SSMEnv("/service/my-service", ssm_client=ssm_client)\n```\n',
    'author': 'Daniel Ancuta',
    'author_email': 'whisller@gmail.com',
    'url': 'https://github.com/whisller/ssmenv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
