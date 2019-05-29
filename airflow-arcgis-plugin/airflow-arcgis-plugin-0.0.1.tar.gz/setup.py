# Package definition file. Use this file to generate a pip package.

from setuptools import find_packages, setup


with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="airflow-arcgis-plugin",
    version="0.0.1",
    author="xyx0826",
    author_email="xyx0826@hotmail.com",
    description="An Apache Airflow plugin to update feature layers from a PostgreSQL database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xyx0826/Airflow-ArcGIS",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Plugins"
    ],
    entry_points={
        'airflow.plugins': [
            'airflow_arcgis = airflow_arcgis.arcgis_plugin:ArcGISPlugin'
        ]
    }
)
