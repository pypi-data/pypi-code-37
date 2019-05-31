import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="validus_pkg_test",
    version="0.0.3",
    author="Stephen McGrath",
    author_email="s_mcgrath1912@live.co.uk",
    description="Case Study Package",
    url="https://github.com/ste645/validus_pkg_test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)