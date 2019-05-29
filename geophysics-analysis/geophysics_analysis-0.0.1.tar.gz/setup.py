import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geophysics_analysis",
    version="0.0.1",
    author="Michael Needham",
    author_email="m.needham@colostate.edu",
    description="A collection of the functions for analysis of geophysical fields",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)