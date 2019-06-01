# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.1'

DESCRIPTION = """
Yet Another Asyncio Requets
""".strip()


setup(name='yaar',
      version=VERSION,
      author='Juca Crispim',
      author_email='juca@poraodojuca.net',
      url='http://myproject.org',
      description=DESCRIPTION,
      packages=find_packages(exclude=['tests', 'tests.*']),
      license='GPL',
      include_package_data=True,
      install_requires=['aiohttp>=3.5.4'],
      test_suite='tests',
      provides=['yaar'],)
