# @Vendors
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nlp_model_gen_plugins',
    version='0.1.1',
    author='Gerardo Alias',
    author_email='alias_gerardo@yahoo.com.ar',
    description='NLP admin plugins',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    url='https://github.com/galias11/nlp_model_gen_plugins',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[]
)
