# --*coding:utf8 *--
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="edrpou",
    version="1.3",
    author="Pavlo Yaremchuk (pablissimo77)",
    author_email="pablissimo77@gmail.com",
    description="Ukrainian EDRPOU-IIN validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pablissimo77/edrpou-iin-validation/",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
)
