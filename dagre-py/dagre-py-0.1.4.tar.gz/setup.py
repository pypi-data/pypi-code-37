# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dagre_py']

package_data = \
{'': ['*'],
 'dagre_py': ['js/d3.v5.min.js',
              'js/d3.v5.min.js',
              'js/d3.v5.min.js',
              'js/d3.v5.min.js',
              'js/d3.v5.min.js',
              'js/d3.v5.min.js',
              'js/dagre-d3.min.js',
              'js/dagre-d3.min.js',
              'js/dagre-d3.min.js',
              'js/dagre-d3.min.js',
              'js/dagre-d3.min.js',
              'js/dagre-d3.min.js',
              'js/index.html',
              'js/index.html',
              'js/index.html',
              'js/index.html',
              'js/index.html',
              'js/index.html',
              'js/script.js',
              'js/script.js',
              'js/script.js',
              'js/script.js',
              'js/script.js',
              'js/script.js',
              'js/style.css',
              'js/style.css',
              'js/style.css',
              'js/style.css',
              'js/style.css',
              'js/style.css',
              'js/tippy.all.min.js',
              'js/tippy.all.min.js',
              'js/tippy.all.min.js',
              'js/tippy.all.min.js',
              'js/tippy.all.min.js',
              'js/tippy.all.min.js']}

setup_kwargs = {
    'name': 'dagre-py',
    'version': '0.1.4',
    'description': 'Thin python wrapper around dagre-d3',
    'long_description': None,
    'author': 'Abhinav Tushar',
    'author_email': 'abhinav@vernacular.ai',
    'url': 'https://github.com/Vernacular-ai/dagre-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
