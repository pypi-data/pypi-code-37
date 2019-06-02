"""Setup script"""
from setuptools import setup, find_packages


with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='keywordtree',
    version='0.1.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3',
    url='https://github.com/tdiam/keywordtree',
    author='Theodoros Diamantidis',
    author_email='diamaltho@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
    ],
)
