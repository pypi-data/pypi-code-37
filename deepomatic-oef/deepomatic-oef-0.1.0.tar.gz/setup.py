import os
import io
from setuptools import find_packages, setup

from deepomatic.oef import VERSION

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements


here = os.path.abspath(os.path.dirname(__file__))

about = {
    '__title__': 'deepomatic-oef',
    '__description__': 'Open Experiment Format',
    '__version__': VERSION,
    '__author__': 'deepomatic',
    '__author_email__': 'support@deepomatic.com',
    '__url__': 'https://github.com/Deepomatic/open-experiment-format',
    '__license__': 'MIT License',
    '__project_urls__': {
        'Product': 'https://deepomatic.com',
        'Source': 'https://github.com/deepomatic/open-experiment-format',
        'Tracker': 'https://github.com/deepomatic/open-experiment-format/issues',
    }
}

with io.open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Read requirements
install_reqs = parse_requirements(os.path.join(here, 'requirements.txt'), session='hack')

namespaces = ['deepomatic']

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    project_urls=about['__project_urls__'],
    license=about['__license__'],
    packages=find_packages(),
    namespace_packages=namespaces,
    include_package_data=True,
    long_description=README,
    long_description_content_type='text/markdown',
    data_files=[('', ['requirements.txt', 'LICENSE'])],
    install_requires=[str(ir.req) for ir in install_reqs],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
