import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sciunivariate",
    version="0.0.1",
    author="gurdit singh",
    author_email="gurdit.singh@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gurditsingh/FirstPython",
    packages=setuptools.find_packages(),
	 install_requires=[
        "texttable >= 1.6.1",
	],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)