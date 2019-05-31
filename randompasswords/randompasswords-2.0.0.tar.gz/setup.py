import setuptools

# README text

with open("README.rst", "r") as f:
    long_description = f.read()

#calling setup()
setuptools.setup(
    name="randompasswords",
    version="2.0.0",
    description="Takes user input and generates random passwords",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/JosephJ12/randompasswords",
    author="Joseph Jung",
    author_email="josephjung12@gmail.com",
    license="MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    #install_requires=["wxPython",],
)