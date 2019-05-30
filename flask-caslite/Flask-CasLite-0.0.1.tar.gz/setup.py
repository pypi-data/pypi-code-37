"""
    Flask-CasLite
    ~~~~~~~~~~~~~~
    
    :author: Jooonwood <jooonwood@gmail.com>
    :copyright: (c) 2019 by Jooonwood.
    :license: MIT, see LICENSE for more details.
"""

from os import path
from codecs import open
from setuptools import setup

basedir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Flask-CasLite',
    version='0.0.1',
    url='https://github.com/jooonwood/flask-caslite',
    license='MIT',
    author='jooonwood',
    author_email='jooonwood@gmail.com',
    description='cas client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',
    packages=['flask_caslite'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Flask',
        'xmltodict',
    ],
    keywords='flask extension development',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)