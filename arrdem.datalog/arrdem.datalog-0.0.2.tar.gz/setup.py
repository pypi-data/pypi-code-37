from setuptools import setup

setup(
    name="arrdem.datalog",
    # Package metadata
    version="0.0.2",
    license="MIT",
    description="A Datalog engine",
    author="Reid 'arrdem' McKenzie",
    author_email="me@arrdem.com",
    url="https://git.arrdem.com/arrdem/datalog-py",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],

    # Package setup
    package_dir={"": "src"},
    packages=[
        "datalog",
    ],
    scripts=["bin/datalog"],
    install_requires=[
    ],
)
