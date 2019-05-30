import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygol",
    version="1.0",
    author="stefan94",
    author_email="stefandevries94@gmail.com",
    description="Conway's Game of Life, made with tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stefandevries94/GameOfLife.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)