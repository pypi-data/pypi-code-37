import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gdtw",
    version="0.0.1",
    author="Dave Deriso",
    author_email="dderiso@stanford.edu",
    description="Package for General Dynamic Time Warping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dderiso/gdtw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)