"""Add support for SoftLayer uploads
"""

from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="monsoon-upload-cos",
    version="0.1.0",
    description="Monsoon plug-in for IBM Cloud Object Storage uploads.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.ibm.com/apset/monsoon",
    author="Michael Lin",
    author_email="michael.lin1@ibm.com",
    license="IBM",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Environment :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Database",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Utilities"
    ],
    packages=find_packages(),
    install_requires=[
        "monsoon-cli>=0.1.7",
        "ibm-cos-sdk>=2.4.4"
    ],
    entry_points={
        "monsoon.uploads": [
            "cos=cos:CloudObjectStorageUpload"
        ]
    }
)
