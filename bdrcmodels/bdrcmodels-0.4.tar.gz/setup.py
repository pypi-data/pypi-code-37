from setuptools import setup, find_packages

setup(name='bdrcmodels',
    version='0.4',
    url='https://github.com/Brown-University-Library/bdrcmodels',
    author='Brown University Library',
    author_email='bdr@brown.edu',
    packages=find_packages(),
    install_requires=[
        'eulfedora>=1.7.2',
        'bdrxml>=1.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
