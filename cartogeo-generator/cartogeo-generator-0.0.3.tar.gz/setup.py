import setuptools
import toml

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = []
pipfile = toml.load("Pipfile")
for package in pipfile["packages"]:
    version = pipfile["packages"][package]
    if version == "*":
        version = ""
    install_requires.append(package + version)

setuptools.setup(
    name="cartogeo-generator",
    version="0.0.3",
    author="David Southgate",
    author_email="d@davidsouthgate.co.uk",
    description="Tool to generate maps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/davidksouthgate/",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    setup_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
