#!/usr/bin/env python

import os
from setuptools import setup, find_packages

setup(name = 'bam_reheader',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.38,
      description = 'reheader a BAM to include GDC @SQ info',
      url = 'https://github.com/jeremiahsavage/bam_reheader/',
      license = 'Apache 2.0',
      include_package_data = True,
      packages = find_packages(),
      install_requires = [
      ],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      entry_points={
          'console_scripts': ['bam_reheader=bam_reheader.__main__:main']
      },
)
