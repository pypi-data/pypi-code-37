import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crossref_commons",
    version="0.0.1",
    author="Crossref",
    author_email="labs@crossref.org",
    description="Crossref Commons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/crossref/crossref_commons_py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
