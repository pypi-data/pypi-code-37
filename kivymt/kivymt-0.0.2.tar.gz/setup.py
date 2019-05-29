#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

if os.name == 'nt': # windows
    preinstall_requires = [
        'docutils',
        'pygments',
        'pypiwin32',
        'kivy.deps.sdl2',
        'kivy.deps.glew',
    ]
else:
    preinstall_requires = []

setup(
    name='kivymt',
    version='0.0.2',
    description="Extra Kivy modules written by Minh-Tri Pham",
    author=["Minh-Tri Pham"],
    #scripts=['scripts/visionml_viewer.py'],
    packages=find_packages(),
    package_data={
        'kivymt': ['data/*'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=preinstall_requires+[
        'basemt', # for logging and multi-threading purposes
        'kivy',
        'kivy-garden',
        'pygame', # for kivy
    ],
)
