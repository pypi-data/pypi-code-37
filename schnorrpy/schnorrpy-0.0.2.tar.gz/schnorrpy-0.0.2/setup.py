#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python package setup tooling."""

# XXX: TODO
# Maybe do packaging as outlined here:
# - https://pypi.org/project/setuptools-rust/

# Other helpful source of info:
# - cookiecutter Rust Py package:
#   https://www.reddit.com/r/Python/comments/6masn0/build_and_release_python_binary_wheels_with_rust/
#   https://github.com/mckaymatt/cookiecutter-pypackage-rust-cross-platform-publish
# - example using the cookie cutter:
#   https://github.com/mckaymatt/rust_pypi_example

from codecs import open
from os import path

from setuptools import setup
from setuptools_rust import Binding, RustExtension


__version__ = '0.0.2'

here = path.abspath(path.dirname(__file__))


def long_description():
    """Get the long description from the README file."""
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()


def install_requires(include_repo_links=True):
    """Get the dependencies and installs."""
    with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        all_reqs = f.read().split('\n')
    packages = [x.strip() for x in all_reqs if 'git+' not in x]
    repo_links = [x.strip().replace('git+', '')
                  for x in all_reqs if x.startswith('git+')]
    if include_repo_links:
        return packages + repo_links
    else:
        return packages


setup(
    name='schnorrpy',
    version=__version__,
    description=('A Python wrapper to the Rust schnorrkel SR25519'
                 ' signature library.'),
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/kauriid/schnorrpy.git',
    license='Apache License 2.0',
    # See here for `classifiers`:
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=('singlesource blockchain substrate centrality polkadot'
              ' signing signature SS25519'),
    rust_extensions=[RustExtension('schnorrpy', 'Cargo.toml',
                                   binding=Binding.PyO3)],
    test_suite='tests',
    packages=['schnorrpy'],
    zip_safe=False,
    include_package_data=True,
    author=['Mischa MacLeod', 'Guy K. Kloss'],
    install_requires=[],
    dependency_links=install_requires(include_repo_links=True),
    author_email='guy@mysinglesource.io'
)
