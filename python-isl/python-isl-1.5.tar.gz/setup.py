from setuptools import setup

long_description = open('README.md').read()


setup(
    name='python-isl',
    version='1.5',
    author='Joseph Solomon',
    author_email='josephs@isl.co',
    description=('A python package to wrap the islapi.'),
    license='MIT',
    keywords='python isl api',
    url='https://github.com/istrategylabs/python-isl',
    packages=['pythonisl', ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=['requests>=2.21,<2.22', 'PyJWT>=1.7.1,<1.8.0'],
)
