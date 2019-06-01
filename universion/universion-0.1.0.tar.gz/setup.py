import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="universion",
    version="0.1.0",
    author="Robert Kennedy",
    author_email="robert076kennedy@gmail.com",
    description="An automated versioning tool using semantic versioning and conventional commits that supports a majority of software project types.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roblkenn/UniVersion",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "universion=universion.cli:cli",
        ],
    },
    install_requires=[
        "Click",
        "GitPython"
    ],
)