import os

from distutils.core import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    setup(
        name='frelang',
        description='Interpreted, statically typed, simple, flexible, embeddable language.',
        version='0.1.0-rc2',
        author='Gustavo Ramos Rehermann (Gustavo6046)',
        author_email='rehermann6046@gmail.com',
        license='The MIT License',

        packages=['fre'],
        long_description=f.read()
    )
