#!/usr/bin/env python

import versioneer
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='python_tooling_example',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Example Python package using Pytest, Sphinx, Travis, Versioneer and Github.',
      long_description=readme(),
      author='Bruno Beltran',
      author_email='brunobeltran0@gmail.com',
      packages=['python_tooling_example',
                'python_tooling_example.example_subpackage'],
      package_data={'python_tooling_example': ['very_large_constants.csv'],
                    'python_tooling_example.example_subpackage': ['very_large_string.txt']},
      license='MIT',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Topic :: Utilities'
      ],
      keywords='python tooling meta example',
      url='https://github.com/brunobeltran/python_tooling_example',
      install_requires=['pandas'],
)
