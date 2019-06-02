# -*- coding: utf-8 -*-

from setuptools import setup, find_namespace_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pytdd',
    version='1.0.0',
    description='python TDD assistant, runs test command on source file change only',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Alex Chauvin',
    author_email='ach@meta-x.org',
    url='https://gitlab.com/achauvinhameau/pytdd',
    # license=license,
    packages=find_namespace_packages('pytdd', 
                                     exclude=('tests', 'docs', 'env36', 'dist')),

    entry_points = {
        'console_scripts': [
            'pytdd = pytdd:main',
        ],
    },

    data_files=[
        ('bin', [
            'pytdd/pytdd.py',
        ]),
    ],

    python_requires='>=3',
    install_requires=['watchdog'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
    ],
)
