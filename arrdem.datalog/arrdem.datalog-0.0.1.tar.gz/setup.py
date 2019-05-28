from setuptools import find_namespace_packages, setup

setup(
    name="arrdem.datalog",
    version="0.0.1",
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
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    scripts=["bin/datalog"]
)
