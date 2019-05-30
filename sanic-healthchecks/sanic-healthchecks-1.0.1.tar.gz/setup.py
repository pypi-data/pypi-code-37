# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sanic_healthchecks']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5,<4.0']

setup_kwargs = {
    'name': 'sanic-healthchecks',
    'version': '1.0.1',
    'description': 'A small wrapper for making it easy to add a healthcheck server to your Sanic application',
    'long_description': '# sanic-healthchecks\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![PyPI version](https://badge.fury.io/py/sanic-healthchecks.svg)](https://badge.fury.io/py/sanic-healthchecks)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/sanic-healthchecks.svg)](https://pypi.python.org/pypi/sanic-healthchecks/)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/sanic-healthchecks.svg)\n\nsanic-healthchecks makes it easy for you to start a healthcheck server on a\ndifferent thread than your actual Sanic application.\n\n## Installation\n\n`pip3 install sanic-healthchecks`\n\n## Healthcheck Example\n```python\nfrom sanic import Sanic\nfrom sanic.response import json\n\nfrom sanic_healthchecks import start_healthcheck_server, healthcheck_response\n\nAPP = Sanic()\n\n\nasync def healthcheck_handler(_):\n    data = {"status": "ok"}\n    return healthcheck_response(data)\n\n\n@APP.route("/")\nasync def root(_):\n    return json({"example_of": "a very simple healthcheck"})\n\n\nif __name__ == "__main__":\n    start_healthcheck_server(healthcheck_handler)\n    APP.run(host="0.0.0.0", port=8000)\n```\n\nYour Sanic application will now respond on to healthchecks on a different port:\n```\n⇒  curl http://localhost:8000 -i\nHTTP/1.1 200 OK\nConnection: keep-alive\nKeep-Alive: 5\nContent-Length: 17\nContent-Type: application/json\n\n{"hello":"world"}\n\n⇒  curl http://localhost:8082 -i\nHTTP/1.1 200 OK\nContent-Type: application/json; charset=utf-8\nContent-Length: 16\nDate: Sun, 03 Mar 2019 20:55:52 GMT\nServer: Python/3.7 aiohttp/3.5.4\n\n{"status": "ok"}\n```\n\n## Changelog\n[Release Changelogs.](https://github.com/abatilo/sanic-healthchecks/blob/master/CHANGELOG.md)\n\n## License\n[Apache 2.0](https://github.com/abatilo/sanic-healthchecks/blob/master/LICENSE)\n\n## But why?\nWhy would you want to run your healthchecks on a different thread, as opposed to creating another endpoint on your actual Sanic server?\n\nGreat question, internet stranger, and I have a few answers.\n\nBy running your healthchecks separately, we maintain a strong separation of\nconcerns. Since Sanic runs on a single thread, then any time you need to\nrespond to healthchecks, you\'re actually taking compute time away from the\nevent loop that is powering the actual requests that your application is there\nto serve. Likewise, the state of your actual application is not going to affect\nthe healthchecks. There\'s a few camps of thought on this subject.\n\nSome people say that if your web service isn\'t capable of responding to your\nhealthcheck probe, then the service shouldn\'t be considered healthy. I can\ntotally understand and respect this perspective, and if this is how you feel,\nthen there\'s no need to use sanic-healthchecks.\n\nOn the other hand, if you\'re like me, you\'ve convinced yourself that the point\nof healthchecks isn\'t purely to determine if the service can respond, but also\nto determine if your service has everything that it needs from downstream\ndependencies. If your requests are taking so long that the readiness or\nliveness probes are timing out, that could mean that your service is unhealthy,\nbut it also could be a symptom of services that have long running requests.\n\nSince we can run the healthchecks on a different web server entirely, we have\nthe ability to check that all of the downstream dependencies, like databases\nand other services, are available. This helps narrow the problems with why a\nservice might be in a degraded state.\n\nI would even make an argument that an increase in response latency could be a\nmetric that you use for automatically scaling your service. Treating it as a\nway to kill instances makes it much fuzzier in terms of how to interpret the\nincrease in latency.\n\nAnother great reason to run your healthchecks on a different server is so that\nyou can assign a different port to this new server. This is valuable because\nyour healthchecks might actually have debug information in them that should not\nbe exposed to the same groups of people who are able to consume the main\nservice. By putting healthchecks on a different port, you can make sure to map\nyour load balancer to **not** include this healthcheck port.\n',
    'author': 'Aaron',
    'author_email': 'AaronBatilo@gmail.com',
    'url': 'https://github.com/abatilo/sanic-healthchecks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
