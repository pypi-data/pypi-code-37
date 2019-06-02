from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name="aihub-deep",
    version="1.0.2",
    description="A Python library for Deep Learning Developers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suvhradipghosh07/Aihub",
    author="Suvhradip Ghosh",
    author_email="suvhradip@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["aihub_deep"],
    include_package_data=True,
    install_requires=["tensorflow","keras","matplotlib","numpy","pandas"],
)
