# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "call-recorder-api"
VERSION = "1.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Call Recorder API",
    author_email="",
    url="https://bitbucket.org/novokrest/python-call-recorder-api.git",
    keywords=["Call Recorder API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Call Recorder API   # noqa: E501
    """
)
