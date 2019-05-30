from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bdcraft-mod-packer',
    version='0.0.3',
    py_modules=['bdcraft_mod_packer'],
    install_requires=['beautifulsoup4', 'fake-useragent', 'lxml', 'requests'],
    url='https://github.com/wafer-li/BDcraft-mod-packer',
    license='Anti 996 License',
    author='Wafer Li',
    author_email='omyshokami@gmail.com',
    description='A tool to download mod patch texture pack in BDcraft.net',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ]
)
