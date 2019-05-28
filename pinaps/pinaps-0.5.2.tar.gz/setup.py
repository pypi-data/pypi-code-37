import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pinaps",
    version="0.5.2",
    author="harri.renney.blino",
    author_email="harri.renney@blino.co.uk",
    description="[BETA]Supporting python package for use with the Blino PiNaps Raspberry pi hat.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/blino-dev/pinaps/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
