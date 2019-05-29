# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from payu_api import VERSION

with open('README.md', 'r') as readme:
    README = readme.read()

setup(
    name = 'django-payu-api',
    version = VERSION.replace(' ', '-'),
    author = 'Integree Bussines Solutions',
    author_email = 'hello@integree.eu',
    description = 'PayU API is a solution that allows you to make payments through the PayU payment gateway.',
    long_description = README,
    long_description_content_type = "text/markdown",
    url = 'https://gitlab.com/integree/payu_api',
    packages = find_packages(),
    include_package_data = True,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 2.7",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires = [
        'django',
        'django-appconf',
        'requests',
    ],
)
