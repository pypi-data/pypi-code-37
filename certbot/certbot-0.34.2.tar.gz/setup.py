import codecs
import os
import re
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

# Workaround for http://bugs.python.org/issue8876, see
# http://bugs.python.org/issue8876#msg208792
# This can be removed when using Python 2.7.9 or later:
# https://hg.python.org/cpython/raw-file/v2.7.9/Misc/NEWS
if os.path.abspath(__file__).split(os.path.sep)[1] == 'vagrant':
    del os.link


def read_file(filename, encoding='utf8'):
    """Read unicode from given file."""
    with codecs.open(filename, encoding=encoding) as fd:
        return fd.read()


here = os.path.abspath(os.path.dirname(__file__))

# read version number (and other metadata) from package init
init_fn = os.path.join(here, 'certbot', '__init__.py')
meta = dict(re.findall(r"""__([a-z]+)__ = '([^']+)""", read_file(init_fn)))

readme = read_file(os.path.join(here, 'README.rst'))
version = meta['version']

# This package relies on PyOpenSSL, requests, and six, however, it isn't
# specified here to avoid masking the more specific request requirements in
# acme. See https://github.com/pypa/pip/issues/988 for more info.
install_requires = [
    'acme>=0.29.0',
    # We technically need ConfigArgParse 0.10.0 for Python 2.6 support, but
    # saying so here causes a runtime error against our temporary fork of 0.9.3
    # in which we added 2.6 support (see #2243), so we relax the requirement.
    'ConfigArgParse>=0.9.3',
    'configobj',
    'cryptography>=1.2.3',  # load_pem_x509_certificate
    # 1.1.0+ is required to avoid the warnings described at
    # https://github.com/certbot/josepy/issues/13.
    'josepy>=1.1.0',
    'mock',
    'parsedatetime>=1.3',  # Calendar.parseDT
    'pyrfc3339',
    'pytz',
    'setuptools',
    'zope.component',
    'zope.interface',
]

dev_extras = [
    'astroid==1.6.5',
    'coverage',
    'ipdb',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'pylint==1.9.4',
    'tox',
    'twine',
    'wheel',
]

dev3_extras = [
    'mypy',
    'typing', # for python3.4
]

docs_extras = [
    # If you have Sphinx<1.5.1, you need docutils<0.13.1
    # https://github.com/sphinx-doc/sphinx/issues/3212
    'repoze.sphinx.autointerface',
    'Sphinx>=1.2', # Annotation support
    'sphinx_rtd_theme',
]


class PyTest(TestCommand):
    user_options = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name='certbot',
    version=version,
    description="ACME client",
    long_description=readme,
    url='https://github.com/letsencrypt/letsencrypt',
    author="Certbot Project",
    author_email='client-dev@letsencrypt.org',
    license='Apache License 2.0',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(exclude=['docs', 'examples', 'tests', 'venv']),
    include_package_data=True,

    install_requires=install_requires,
    extras_require={
        'dev': dev_extras,
        'dev3': dev3_extras,
        'docs': docs_extras,
    },

    # to test all packages run "python setup.py test -s
    # {acme,certbot_apache,certbot_nginx}"
    test_suite='certbot',
    tests_require=["pytest"],
    cmdclass={"test": PyTest},

    entry_points={
        'console_scripts': [
            'certbot = certbot.main:main',
        ],
        'certbot.plugins': [
            'manual = certbot.plugins.manual:Authenticator',
            'null = certbot.plugins.null:Installer',
            'standalone = certbot.plugins.standalone:Authenticator',
            'webroot = certbot.plugins.webroot:Authenticator',
        ],
    },
)
