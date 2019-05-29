from distutils.core import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py-toolbox',
    version='0.1.3',
    author='Daniel Grießhaber',
    author_email='dangrie158@gmail.com',
    url='https://github.com/dangrie158/py-toolbox',
    packages=['pytb', 'pytb.test'],
    license='MIT',
    description='A collection of commonly used python snippets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
