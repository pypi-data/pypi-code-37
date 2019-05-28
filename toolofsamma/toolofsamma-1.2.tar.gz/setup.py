from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='toolofsamma',
    version='1.2',
    packages=setuptools.find_packages(),
    author='samma',
    author_email='1570858572@qq.com',
    description='the private tool of samma',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
