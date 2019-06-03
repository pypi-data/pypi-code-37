from setuptools import setup, find_packages

setup(
    name="feb",
    version="0.1",

    install_requires=[
        "Click>6",
        'requests'
    ],

    url="",
    author="freeaquar",
    author_email="freeaquar@163.com",
    description="fast env builder",
    license="MIT Licence",
    keywords="fast env",

    packages=find_packages(where='src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'': 'src'},

    py_modules=['bootstrap'],

    entry_points={
        "console_scripts": [
            "feb = bootstrap:main",
        ],
        "gui_scripts": [
        ]
    },
)
