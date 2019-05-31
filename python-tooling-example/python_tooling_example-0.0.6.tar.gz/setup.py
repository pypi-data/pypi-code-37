#!/usr/bin/env python

import versioneer # replace with import package_name if not using versioneer
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='python_tooling_example', # importable name of package
      version=versioneer.get_version(), # use package_name.__version__ if no versioneer
      cmdclass=versioneer.get_cmdclass(), # omit if not using versioneer
      # a short description of your package
      description='Example Python package using Pytest, Sphinx, Travis, Versioneer and Github.',
      # make sure to create a README.rst file for you package, it will serve as
      # the landing page for the package on PyPI and Github.
      long_description=readme(),
      # a couple of self-explanatory fields
      author='Bruno Beltran',
      author_email='brunobeltran0@gmail.com',
      # an explicit listing of each package to be included when uploading to
      # PyPI
      packages=['python_tooling_example',
                'python_tooling_example.example_subpackage'],
      # if any of the packages require non-python (e.g. binary or csv) files to
      # work correctly, specify their locations here (relative to that
      # package's directory)
      package_data={'python_tooling_example': ['very_large_constants.csv'],
                    'python_tooling_example.example_subpackage': ['very_large_string.txt']},
      # licence type, MIT is very permissive
      license='MIT',
      # see the setuptools docs for what kinds of things can go here
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Topic :: Utilities'
      ],
      # whatever you see fit to tag the project with
      keywords='python tooling meta example',
      # package-name.rtfd.io and github.com/user/package_name are good choices
      url='https://github.com/brunobeltran/python_tooling_example',
      # list any packages that this one requires for it to work
      # if this is non-empty, make sure you also have a requirements.txt file
      # that simply contains a single period (i.e. ".") character. if there are
      # any dependencies that are required to test/deploy/build your package
      # but are not required to actually use it, those belong in
      # requirements_dev.txt, not here.
      install_requires=['pandas'],
)
