import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="ramses-wolasoft",
    version="0.0.2",
    author="Komi Wolanyo KOUDO",
    author_email="wolasoft@wolasoft.com",
    description="A small flask based restful ramses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="flask, server, rest",
    url="https://github.com/wolasoft/ramses",
    packages=setuptools.find_packages(),
    install_requires=[
        'Flask==1.0.3',
        'Flask-Cors==3.0.7',
        'Flask-Log-Request-ID==0.10.0',
        'stringcase==1.2.0'
    ],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
