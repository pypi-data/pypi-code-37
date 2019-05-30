import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colosseumrl",
    version="1.0.0",
    author="Alexander Shmakov",
    author_email="alexanders101@gmail.com",
    description="UC Irvine multi-agent reinforcement learning framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/colosseumrl/Colosseum",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)