import setuptools
import cli_configparser

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='cli-configparser',
    version=cli_configparser.version,
    author='Denis Newman-Griffis',
    author_email='denis.newman.griffis@gmail.com',
    description='CLI utility for reading from .ini config files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/drgriffis/cli-configparser',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
