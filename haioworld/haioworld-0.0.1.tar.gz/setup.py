import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()
	
setuptools.setup(
    name="haioworld",
    version="0.0.1",
    author="Nagalatha",
    author_email="nagalatha@gmail.com",
    description="Say hello!",
    py_modules=["haiworld"],
    package_dir={'' : 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohitaradhya",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


