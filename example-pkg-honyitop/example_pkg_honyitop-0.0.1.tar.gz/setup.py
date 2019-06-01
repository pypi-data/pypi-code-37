import setuptools

with open ( "README.md" , "r" ) as fh :
    long_description = fh . read ()

setuptools . setup (
    name = "example_pkg_honyitop" ,
    version = "0.0.1" ,
    author = "honyi" ,
    author_email = "18201245243@163.com" ,
    description = "A small example package for abc." ,
    long_description = long_description ,
    long_description_content_type = "text/markdown" ,
    url = "https://github.com/pypa/sampleproject" ,
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3" ,
        "License :: OSI Approved :: MIT License" ,
        "Operating System :: OS Independent" ,
    ],
)
