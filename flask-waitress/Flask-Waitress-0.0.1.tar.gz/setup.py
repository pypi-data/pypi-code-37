from setuptools import setup

version = '0.0.1'

setup(
    name="Flask-Waitress",
    version=version,
    py_modules=["flask_waitress"],
    install_requires=['flask>=0.9', 'paste>=1.7', 'waitress'],
    author="Charlie Wolf",
    author_email="charlie@wolf.is",
    description="Flask Waitress",
    license="Tequilaware",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: Utilities",
    ]
)