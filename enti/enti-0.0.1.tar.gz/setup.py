import setuptools
from enti.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="enti",
    version=__version__,
    author="Joe Goulet",
    author_email="joseph.goulet@istresearch.com",
    description="A toolkit for unstructured text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/istresearch/enti",
    packages=setuptools.find_packages(exclude=[
        "*.test*", "*.lexicons*", "*.pipelines*"
    ]),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "nltk",
        "numpy"
    ],
    include_package_data=False,
    entry_points={}
)
