# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.1.1'

DESCRIPTION = """
Yet Another Asyncio Requets
""".strip()


setup(name='yaar',
      version=VERSION,
      author='Juca Crispim',
      author_email='juca@poraodojuca.net',
      url='https://pypi.python.org/pypi/yaar',
      description=DESCRIPTION,
      long_description=DESCRIPTION,
      py_modules=['yaar'],
      license='GPL',
      include_package_data=True,
      install_requires=['aiohttp>=3.5.4'],
      test_suite='tests',
      provides=['yaar'],)
