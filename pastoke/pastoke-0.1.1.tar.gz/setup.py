import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='pastoke',
    version='0.1.1',
    author="streanger",
    author_email="divisionexe@gmail.com",
    description="paste jokes script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/streanger/pastoke",
    packages=['pastoke',],
    license='MIT',
    install_requires=['pyperclip'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)