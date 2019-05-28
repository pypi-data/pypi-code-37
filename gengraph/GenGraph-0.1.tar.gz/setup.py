import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GenGraph",
    version="0.1",
    author="Jon Ambler",
    author_email="jambler24@gmail.com",
    description="Tools for the creation and use of genome graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jambler24/GenGraph",
    packages=setuptools.find_packages(),
    install_requires=[
          'networkx',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
