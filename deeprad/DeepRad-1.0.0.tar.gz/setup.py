import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DeepRad",
    version="1.0.0",
    author="MIMRTL Lab",
    author_email="mimrtl.uwmadison@gmail.com",
    description="A toolbox of Deep Learning in Medical Images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mimrtl/DeepRad",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
)
