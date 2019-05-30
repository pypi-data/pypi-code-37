from setuptools import setup

setup(
    name='mapp-airflow-extensions',
    version='0.01',
    descriptions='A library with some airflow extensions',
    author='Caio Belfort',
    author_email='caiobelfort90@gmail.com',
    license='GPL',
    packages=['mapp'],
    zip_safe=False,
    install_requires=[
        'apache-airflow[gcp_api]>=1.10.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
    ]
)

