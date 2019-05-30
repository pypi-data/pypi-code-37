#!/usr/bin/env python3

# std
from distutils.core import setup

# noinspection PyUnresolvedReferences
import setuptools  # see below (1)
from pathlib import Path

# (1) see https://stackoverflow.com/questions/8295644/
# Without this import, install_requires won't work.


keywords = [
    "clustering",
    "cluster",
    "kinematics",
    "cluster-analysis",
    "machine-learning",
    "ml",
    "hep",
    "hep-ml",
    "hep-ex",
    "hep-ph",
    "wilson",
    "clusterking"
]

description = (
    "Physics distributions to be clustered by the ClusterKinG package."
)

this_dir = Path(__file__).resolve().parent

packages = setuptools.find_packages()

with (this_dir / "README.rst").open() as fh:
    long_description = fh.read()

with (this_dir / "clusterking_physics" / "version.txt").open() as vf:
    version = vf.read()

with (this_dir / "requirements.txt").open() as rf:
    install_requires = [
        req.strip()
        for req in rf.readlines()
        if req.strip() and not req.startswith("#")
    ]


setup(
    name="clusterking_physics",
    version=version,
    packages=packages,
    install_requires=install_requires,
    url="https://github.com/clusterking/clusterking_physics",
    project_urls={
        "Bug Tracker": "https://github.com/clusterking/clusterking_physics/issues",
        "Source Code": "https://github.com/clusterking/clusterking_physics/",
    },
    package_data={"clusterking_physics": ["version.txt"]},
    license="MIT",
    keywords=keywords,
    description=description,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics"
    ],
)

