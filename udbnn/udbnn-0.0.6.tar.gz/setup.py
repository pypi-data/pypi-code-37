import os
import re
import sys
# To use a consistent encoding
from codecs import open as copen
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with copen(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def read(*parts):
    with copen(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("udbnn", "__version__.py")

test_deps =["pytest-cov", "validate_version_code", "codacy-coverage", "coveralls", "pytest"]

extras = {
    'test': test_deps,
}

setup(
    name='udbnn',
    version=__version__,
    description="Experiment to determine whetever a large batch-size can be helpful with extremely umbalanced datasets.",
    long_description=long_description,
    url="https://github.com/LucaCappelletti94/udbnn",
    author="Luca Cappelletti",
    author_email="cappelletti.luca94@gmail.com",
    # Choose your license
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    tests_require=test_deps,
    # Add here the package dependencies
    install_requires=["keras_tqdm", "keras", "sklearn", "extra_keras_utils", "notipy_me", "holdouts_generator", "extra_keras_metrics", "auto_tqdm", "pandas", "tqdm", "silence_tensorflow"],
    extras_require=extras,
)