import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DeezerPy",
    version="1.0",
    author="Nicolas Villalobos",
    author_email="developmentvilla@gmail.com",
    description="Wrapper for the Deezer API including authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NcVillalobos/DeezPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)