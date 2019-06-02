# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fanfic_scraper', 'fanfic_scraper.extractors']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.7,<5.0',
 'fake_useragent>=0.1.11,<0.2.0',
 'html2text>=2018.1,<2019.0',
 'html5lib>=1.0,<2.0',
 'pony>=0.7.10,<0.8.0',
 'pysocks>=1.7,<2.0',
 'requests>=2.22,<3.0',
 'tldextract>=2.2,<3.0']

entry_points = \
{'console_scripts': ['fanfic-scraper = fanfic_scraper.fanfic_scraper:main',
                     'ff = fanfic_scraper.ff:main',
                     'ff-fif = fanfic_scraper.ff_fif:main',
                     'ff-h2t = fanfic_scraper.ff_h2t:main',
                     'ff-rf = fanfic_scraper.ff_rf:main',
                     'ffdl = fanfic_scraper.ffdl:main']}

setup_kwargs = {
    'name': 'fanfic-scraper',
    'version': '0.7.4',
    'description': 'Scrapes fanfics, maintains download db, organizes folders when reading.',
    'long_description': None,
    'author': 'Kevin Meredith',
    'author_email': 'kevin@meredithkm.info',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
