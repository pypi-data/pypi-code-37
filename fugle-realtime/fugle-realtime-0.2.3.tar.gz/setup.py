# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fugle_realtime']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.24.2,<0.25.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'fugle-realtime',
    'version': '0.2.3',
    'description': 'Fugle Realtime',
    'long_description': '# fugle-realtime-py\n\nFugle Realtime Python is a Python package to query realtime stock quote of Taiwan market through API provided by [Fugle](https://www.fugle.tw/).\n\nCurrently supported exchanges are [Taiwan Stock Exchange (TWSE)](http://www.twse.com.tw/) and [Taipei Exchange(TPEx)](https://www.tpex.org.tw/).\n\n## Documentations\n\n-  [Fugle Developer](https://developer.fugle.tw/)\n\n    - https://developer.fugle.tw/realtime\n\n-  [PyPI](https://pypi.org/)\n\n    - https://pypi.org/project/fugle-realtime/\n\n## Installation\n\n```sh\npip install fugle-realtime\n```\n\nThis package is compatible with Python 3.6 or higher.\n\n## Usage\n\n```py\nfrom fugle_realtime import intraday\n```\n\n### [`intraday.chart`](https://developer.fugle.tw/realtime/document#/Intraday/get_intraday_chart): https://api.fugle.tw/realtime/v0/intraday/chart\n\n```py\nintraday.chart(apiToken="demo", output="dataframe", symbolId="2884")\n```\n\n### [`intraday.meta`](https://developer.fugle.tw/realtime/document#/Intraday/get_intraday_meta): https://api.fugle.tw/realtime/v0/intraday/meta\n\n```py\nintraday.meta(apiToken="demo", output="dataframe", symbolId="2884")\n```\n\n### [`intraday.quote`](https://developer.fugle.tw/realtime/document#/Intraday/get_intraday_quote): https://api.fugle.tw/realtime/v0/intraday/quote\n\n```py\nintraday.quote(apiToken="demo", output="dataframe", symbolId="2884")\n```\n\n### [`intraday.trades`](https://developer.fugle.tw/realtime/document#/Intraday/get_intraday_trades): https://api.fugle.tw/realtime/v0/intraday/trades\n\n```py\nintraday.trades(apiToken="demo", output="dataframe", symbolId="2884")\n```\n\n`output="dataframe"` will return [pandas](https://pandas.pydata.org/) [`DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html), which is the default. `output="raw"` will return [python](https://www.python.org/) built-in [`dict`](https://docs.python.org/3/library/stdtypes.html#dict) or [`list`](https://docs.python.org/3/library/stdtypes.html#list) accordingly.\n\n`symbolId="2884"` is only allowed when `apiToken="demo"`. To access more `symbolId`, you will have to get your own `apiToken`. Please visit https://developer.fugle.tw/realtime/apiToken for detailed instructions.\n\nFor complete documentation of each URL and its parameters in association with the corresponding function and its arguments specified above, please visit https://developer.fugle.tw/realtime/document.\n',
    'author': 'Fortuna Intelligence Co., Ltd.',
    'author_email': 'development@fugle.tw',
    'url': 'https://developer.fugle.tw/realtime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
