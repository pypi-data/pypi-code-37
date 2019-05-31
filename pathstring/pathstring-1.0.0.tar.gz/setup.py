# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['pathstring']
setup_kwargs = {
    'name': 'pathstring',
    'version': '1.0.0',
    'description': 'String with path operations.',
    'long_description': '|pypi| |support| |license| |pipelines| |black|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/pathstring.svg?style=flat-square\n    :target: https://pypi.org/project/pathstring/\n    :alt: PyPI version.\n\n.. |support| image:: https://img.shields.io/pypi/pyversions/pathstring.svg?style=flat-square\n    :target: https://pypi.org/project/pathstring/\n    :alt: Supported Python versions.\n\n.. |license| image:: https://img.shields.io/pypi/l/pathstring.svg?style=flat-square\n    :target: https://pypi.org/project/pathstring/\n    :alt: Project license.\n\n.. |pipelines| image:: https://dev.azure.com/uyar0839/pathstring/_apis/build/status/uyar.pathstring?branchName=master\n    :target: https://dev.azure.com/uyar0839/pathstring/_build\n    :alt: Azure Pipelines build status.\n\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square\n    :target: https://github.com/python/black\n    :alt: Code formatted by Black.\n\n\npathstring is a very small module that provides only one class\n(``pathstring.Path``) which is a string with support for path operations.\nTechnically, it subclasses ``str`` and delegates path related operations to\n``pathlib.Path``.\n\nDifferences from pathlib paths are:\n\n- Paths are strings, no need to cast them to strings.\n\n- No distinction between "pure" and "concrete" paths.\n\n- No explicit distinction between Posix and Windows paths, but paths are\n  always "native" to their platform.\n\n- Adds a ``Path.rmtree()`` method which invokes ``shutil.rmtree()``\n  on the path. Actually, since paths are strings, ``shutil.rmtree(path)``\n  will also work.\n\n- Adds a ``strict`` parameter to the ``Path.relative_to()`` method\n  which, when set to ``False``, will also navigate "up" in the hierarchy.\n\n- No support for case-insensitive comparisons on Windows.\n\n- No ``Path.replace()`` method since it would cause confusion with\n  ``str.replace()``.\n\nFeatures are tested extensively against `pathlib documentation`_ to guarantee\ncompatibility.\n\nLicense\n-------\n\nCopyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>\n\npathstring is released under the BSD license. Read the included\n``LICENSE.txt`` file for details.\n\n.. _pathlib documentation: https://docs.python.org/3/library/pathlib.html\n',
    'author': 'H. Turgut Uyar',
    'author_email': 'uyar@tekir.org',
    'url': 'https://pypi.org/project/pathstring/',
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
