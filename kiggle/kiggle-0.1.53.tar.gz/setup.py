import setuptools
import re

VERSIONFILE = "./kiggle/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)

if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

with open("README.md", "rb") as fh:
    long_description = fh.read().decode('utf-8', errors='ignore')

setuptools.setup(
    name="kiggle",
    version=verstr,
    author="Aakash N S (Jovian)",
    author_email="hello@jvn.io",
    description="Utility functions for data science competitions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aakashns/kiggle",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
