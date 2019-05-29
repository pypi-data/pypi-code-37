from setuptools import setup

setup(
    name="pdl",
    version="0.8.18",
    author="Zero to singularity",
    author_email="jan@zerotosingularity.com",
    install_requires=['requests>=2.18.4'],
    url="https://github.com/zerotosingularity/pdl",
    description="Public Download Library",
    long_description="Download public datasets in one line of code",
    license="MIT",
    packages=['pdl']
)
