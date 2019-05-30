# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pytel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytel-inject',
    'version': '0.2.0',
    'description': 'Injection of dependencies for python 3',
    'long_description': 'A bag of objects for Python\n===========================\n\n.. image:: https://img.shields.io/pypi/v/mattes-allegro-pl.svg\n    :target: https://pypi.org/project/mattes-allegro-pl/\n\n.. image:: https://travis-ci.com/mattesilver/pytel.svg\n  :target: https://travis-ci.com/mattesilver/pytel\n\n.. image:: https://codecov.io/gh/mattesilver/pytel/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/mattesilver/pytel\n\nFor when your object graph is too big\n\n.. code-block:: python\n\n  class A:\n    def __init__(self, context: Pytel):\n        self.b = context.b\n\n  class B:\n      pass\n\n  context = Pytel()\n  context.a = lazy(A)(context)\n  context.b = lazy(B)\n\n  assert context.a.b == context.b\n\nWorks with dependency cycles (through a proxy object):\n\n.. code-block:: python\n\n  class A:\n    def __init__(self, context: Pytel):\n      self.b = context.b\n\n  class B:\n    def __init__(self, context: Pytel):\n      self.a = context.a\n\n  context = Pytel()\n  context.a = lazy(A)(context)\n  context.b = lazy(B)(context)\n  \n  assert context.a.b == context.b\n  assert context.b.a == context.a\n  \n',
    'author': 'Rafal Krupinski',
    'author_email': None,
    'url': 'https://github.com/mattesilver/pytel',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
