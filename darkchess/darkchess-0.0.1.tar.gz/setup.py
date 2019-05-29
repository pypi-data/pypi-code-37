import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

reqs = ["numpy", "sty", "mock", "pytest"]

setuptools.setup(
    name="darkchess",
    version="0.0.1",
    author="Vishal Subbiah",
    author_email="subbiahvishal@gmail.com",
    description="incomplete information chess",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vishalsubbiah/darkchess",
    packages=setuptools.find_packages(),
    install_requires=reqs,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
