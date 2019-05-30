import setuptools

with open("README.md" , "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fais",
    version="0.0.5",
    author="Nattapon Donratanapat",
    author_email="pleuk5667@gmail.com",
    description="USGS and Twitter data gathering and analysis tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VidyaSamadi/Research-Team-private",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas==0.23.4',
        'numpy==1.15.4',
        'rpy2==2.9.4',
        'urllib3==1.24.1',
        'requests==2.21.0',
        'opencv-python==4.0.0.21',
        'netCDF4==1.4.2',
        'matplotlib==3.0.2',
        'textblob==0.15.2',
        'pyquery==1.4.0',
        'tweepy==3.7.0',
    ]
)