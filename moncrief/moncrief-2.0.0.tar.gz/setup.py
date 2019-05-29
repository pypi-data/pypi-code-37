import setuptools

setuptools.setup(
    name='moncrief',
    version='2.0.0',
    url='https://github.com/AlgernonSolutions/algernon',
    license='GNU Affero General Public License v3.0',
    author='algernon_solutions/jcubeta',
    author_email='jcubeta@algernon.solutions',
    description='This library contains the basic units of functionality and infrastructure needed to effectively run '
                'operations and applications in a distributed and severless fashion.',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'aws-xray-sdk==2.4.2',
        'boto3==1.9.153',
        'botocore==1.12.153',
        'certifi==2019.3.9',
        'chardet==3.0.4',
        'docutils==0.14',
        'future==0.17.1',
        'idna==2.8',
        'jmespath==0.9.4',
        'jsonpickle==1.1',
        'jsonref==0.2',
        'python-dateutil==2.8.0',
        'python-rapidjson==0.7.1',
        'pytz==2019.1',
        'requests==2.22.0',
        's3transfer==0.2.0',
        'six==1.12.0',
        'urllib3==1.24.3',
        'wrapt==1.11.1'
    ],
)
