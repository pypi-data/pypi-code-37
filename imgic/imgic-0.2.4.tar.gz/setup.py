from setuptools import setup, find_namespace_packages

setup(
    name = "imgic",
    version = "0.2.4",
    description = "A basic numpy-based image manipulation package. Contains tools for resizing, cropping, blurring, and others.",
    url = "https://github.com/LukasNorbutas/imgic",
    author = "Lukas Norbutas",
    author_email = "lukas.norbutas@gmail.com",
    classifiers = ['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7'],
    packages = find_namespace_packages(),
    python_requires = ">=3.5, <4",
    install_requires = ['numpy==1.16.3']
)
