import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="haip-config",
    version="0.1.9",
    author="Reinhard Hainz",
    author_email="reinhard.hainz@gmail.com",
    description="A simple yaml config manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haipdev/config",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "poyo>=0.4.2"
    ]
)
