import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noodle-logging",
    version="0.1",
    author="Askar",
    author_email="aliaskar1024@gmail.com",
    description="Logging to JSON the easy way!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        'six==1.12.0',
        'structlog==19.1.0',
        'python-json-logger==0.1.11'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
