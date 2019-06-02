from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="demohub",
    version="1.0.1",
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
    packages=["demohub"],
    include_package_data=True,
    install_requires=["tensorflow","keras","matplotlib","numpy","pandas"],
)
