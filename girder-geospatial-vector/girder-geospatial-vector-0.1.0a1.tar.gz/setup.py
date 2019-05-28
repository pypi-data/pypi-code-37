from setuptools import setup

setup(
    name='girder-geospatial-vector',
    version='0.1.0a1',
    description='Grid data types for the girder-geospatial package',
    url='https://github.com/OpenGeoscience/girder_geospatial',
    maintainer='Kitware, Inc.',
    maintainer_email='kitware@kitware.com',
    entry_points={
        'geometa.types': [
            'vector=geometa_vector.schema:handler'
        ]
    },
    packages=[
        'geometa_vector'
    ],
    install_requires=[
        'girder-geospatial'
    ]
)
