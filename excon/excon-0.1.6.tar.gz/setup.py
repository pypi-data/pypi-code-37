# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, Extension, find_packages


with open('/Users/RT/projects/excon/README.rst') as f:
    readme = f.read()

setup(
    name='excon',
    version='0.1.6',
    description='Extract and convert data from PDFs',
    long_description="this is a long description of the module",
    long_description_content_type="text/plain",
    author='Ryan Trigg',
    author_email='rbutustree@gmail.com',
    url='https://github.com/rbutus/excon.git',
    license="MIT License",
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'Wand', 'subprocess.run', 'PyPDF2','tabula-py'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
    ],
)

