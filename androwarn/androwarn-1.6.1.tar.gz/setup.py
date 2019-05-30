#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='androwarn',
      version='1.6.1',
      description='Yet another static code analyzer for malicious Android applications',
      long_description_content_type='text/markdown; charset=UTF-8;',
      long_description=open('androwarn/README.md').read(),
      url='https://github.com/maaaaz/androwarn',
      author='Thomas D.',
      author_email='tdebize@mail.com',
      license='LGPL',
      classifiers=[
        'Topic :: Security',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)'],
      keywords='androwarn android apk dalvik static malicious behaviours behaviors reverse disassemble',
      packages=find_packages(),
      install_requires=['androguard >= 3.2.1', 'argparse', 'future', 'jinja2', 'play_scraper'],
      python_requires='>=2.7',
      entry_points = {
        'console_scripts': ['androwarn=androwarn.androwarn:main'],
      },
      include_package_data=True)