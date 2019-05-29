# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['rarbg']
install_requires = \
['aiohttp>=3.5,<4.0',
 'click>=7.0,<8.0',
 'humanize>=0.5.1,<0.6.0',
 'jinja2>=2.10,<3.0',
 'python-dateutil>=2.8,<3.0']

entry_points = \
{'console_scripts': ['rarbg = rarbg:main']}

setup_kwargs = {
    'name': 'rarbg',
    'version': '1.2.1',
    'description': 'RSS interface to TorrentAPI',
    'long_description': '# rarbg → rss\n\nAdapter for Torrent API ([see docs](https://torrentapi.org/apidocs_v2.txt)) that serves search results as broadcatching-ready RSS feed.\n\n## Installation\n\nRequires Python 3.6 or later.\n\n```\npip install -U rarbg\n```\n\n## Docker\n\nRun it with docker like this:\n\n```\ndocker build . --tag rarbg:v1\ndocker run -p 4444:4444 -it rarbg:v1\n```\n\n## Usage\n\nRun the server by typing `rarbg`. You can optionally specify host and port with `-h` (default 0.0.0.0) and `-p` options (default 4444).\n\nAccess it by passing parameters to `http://localhost:444/` as you would pass them to Torrent API.\n\nNote that Torrent API has a rate limit of one request per two seconds.\n\nToken updates and rate limits are handled automatically.\n\n### Convenience methods\n\n`/imdb/<imdb_id>` search by imdb (equals to `/?mode=search&search_imdb=<imdb_id>`)\n\n`/tvdb/<tvdb_id>` search by tvdb (equals to `/?mode=search&search_tvdb=<tvdb_id>`)\n\n`/search/<search_term>` search by string (equals to `/?mode=search&search_string=<search_term>`)\n\n### Available filters\n\n`category` filter by category, specify multiple categories like this:  `44;45`\n\n`limit` number of results: `25`, `50` or `100` (default: `25`)\n\n`sort` order by `seeders`, `leechers` (default: `last`)\n\n`min_seeders` and `min_leechers` hide results with less activity\n\n`ranked=0` get non-scene releases\n\nAll parameters can be mixed together and work with convenience methods.\n\n### Example\n\n`http://localhost:4444/imdb/tt2802850?category=41` will get you HD releases of Fargo\n\n### Categories\n\n```\n 4 XXX (18+)\n14 Movies/XVID\n48 Movies/XVID/720\n17 Movies/x264\n44 Movies/x264/1080\n45 Movies/x264/720\n47 Movies/x264/3D\n42 Movies/Full BD\n46 Movies/BD Remux\n18 TV Episodes\n41 TV HD Episodes\n23 Music/MP3\n25 Music/FLAC\n27 Games/PC ISO\n28 Games/PC RIP\n40 Games/PS3\n32 Games/XBOX-360\n33 Software/PC ISO\n35 e-Books\n```\n',
    'author': 'banteg',
    'author_email': 'banteeg@gmail.com',
    'url': 'https://github.com/banteg/rarbg',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
