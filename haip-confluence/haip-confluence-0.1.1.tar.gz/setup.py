import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="haip-confluence",
    version="0.1.1",
    author="Reinhard Hainz",
    author_email="reinhard.hainz@gmail.com",
    description="A Confluence API client.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haipdev/confluence",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "aiohttp",
        "haip-config",
        "haip-template"
    ]
)
