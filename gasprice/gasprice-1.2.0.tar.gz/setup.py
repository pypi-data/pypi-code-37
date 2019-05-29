# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['gasprice']
install_requires = \
['click>=7.0,<8.0',
 'pandas>=0.24.2,<0.25.0',
 'retry>=0.9.2,<0.10.0',
 'sanic>=19.3,<20.0',
 'web3>=4.9,<5.0']

entry_points = \
{'console_scripts': ['gasprice = gasprice:main']}

setup_kwargs = {
    'name': 'gasprice',
    'version': '1.2.0',
    'description': 'predict ethereum gas price',
    'long_description': '# gasprice\n\nestimates ethereum gas price based on recent blocks and provides a simple api\n\n## hosted\n\n- https://gasprice.poa.network (kindly deployed by [poa network](https://poa.network))\n\n## installation\n\nrequires python 3.6 and an ethereum full node. infura.io won\'t work as it doesn\'t allow setting up `filter`.\n\n```bash\npip install gasprice\n```\n\nthere is an example of systemd service if you want to run it as a service.\n\n## usage\n\n```bash\ngasprice\n\nOptions:\n  -h, --host 127.0.0.1\n  -p, --port 8000\n  -s, --skip-warmup\n```\n\nethereum rpc url can be set with `ETH_RPC_URL` environment variable (default `http://localhost:8545`).\n\n## api\n\n```json\n{\n  "block_number": 4813900,\n  "block_time": 14.9,\n  "health": true,\n  "slow": 1,\n  "standard": 4,\n  "fast": 20,\n  "instant": 40\n}\n```\n\n`slow`, `standard`, `fast` and `instant` values represent minimal gas price of the latest 200 blocks. by default slow represents 30% probability, standard is 60%, fast is 90% and instant is 100%.\n',
    'author': 'banteg',
    'author_email': 'banteeg@gmail.com',
    'url': 'https://github.com/banteg/gasprice',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
