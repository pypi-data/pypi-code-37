from setuptools import setup, find_namespace_packages,find_packages
# import os

# base_dir = os.path.dirname(os.path.abspath(__file__))
# requirements_file = open(os.path.join(base_dir, 'requirements.txt'))
# requirements = requirements_file.read().splitlines()
"""
python setup.py bdist_wheel 生成 wheel文件
python setup.py sdist 生成压缩包
twine upload dist/*
"""
setup(
    name="treelab",
    version="1.2.4",
    # package_dir={'': 'src'},
    # packages=find_namespace_packages(where='src'),
    packages=find_packages(exclude=["tests"]),
    install_requires=['Rx>=3.0.0a3', 'grpcio>=1.20.0', 'grpcio-tools>=1.20.0', 'pandas>=0.24.2'],
    python_requires='>=3',
    zip_safe=True,
    license='BSD License',
    url='https://caminerinc.github.io/treelab-pySDK/',
    long_description='The Treelab Python API provides an easy way to integrate Treelab with any external system. The API closely follows REST semantics, uses JSON to encode objects, and relies on standard HTTP codes to signal operation outcomes.'
)