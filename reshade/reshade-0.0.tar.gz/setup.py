from setuptools import setup, find_packages

def readme():
    with open("README.rst") as f:
        return f.read()
        
exec(open("reshade/_version.py").read())

setup(
    name="reshade",
    version=__version__,
    description="Reshade is a library to create low-level convolutional neural networks",
    long_description=readme(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="reshade artificial intelligence",
    url="https://github.com/jamesjiang52/Reshade",
    author="James Jiang",
    author_email="jamesjiang52@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
