
from setuptools import setup

from objectvalidator import __version__ as VERSION


description = (
    'Decorator for validating and caching values returning from methods.'
)

try:
    long_description = open('README.rst', 'rb').read().decode('utf-8')
except IOError:
        long_description = description

setup(
    name='objectvalidator',
    version=VERSION,
    author='Jan Seifert (Seznam.cz, a.s.)',
    author_email='jan.seifert@firma.seznam.cz',
    description=description,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license='BSD',
    url='https://blog.seznam.cz/stitek/vyvojari/',
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    platforms=['any'],
    py_modules=['objectvalidator'],
    zip_safe=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
