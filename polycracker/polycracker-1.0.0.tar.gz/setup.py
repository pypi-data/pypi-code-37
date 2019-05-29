
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='polycracker',
    version='1.0.0',
    author='polycracker team',
    author_email='sgordon@lbl.gov',
    description='unsupervised classification of polyploid subgenomes',
    long_description='README.md',
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/berkeleylab/jgi-polycracker",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "polycracker=polycracker.polycracker:polycracker",
        ]
    },
)
