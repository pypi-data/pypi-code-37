# -*-coding: utf-8-*-
import pathlib

import setuptools

README = (pathlib.Path(__file__).parent / "README.md").read_text()
setuptools.setup(
    name="hbdl",
    version="0.0.1",
    author="unkloud",
    author_email="unkloud.com.au@gmail.com",
    description="Another humble bundle downloader",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/unkloud/hbdl.git",
    packages=setuptools.find_packages(),
    install_requires=["requests==2.22.0", "click==7.0"],
    entry_points={"console_scripts": ["hbdl=hbdl.hbdl:download"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
