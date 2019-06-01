import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maxFstoolkit",
    version="0.0.1",
    author="Maxwell Flitton",
    author_email="maxwellflitton@gmail.com",
    description="Basic package that wraps dataframes and lists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxwellflitton/maxFstoolkit",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Build Tools"
    ),
    install_requires=[
        "numpy==1.16.4",
        "pandas==0.24.2",
        "discord-webhook==0.4.1",
        "idna==2.8",
        "peewee==3.9.5",
        "requests==2.22.0",
        "urllib3==1.25.2"
    ],
    zip_safe=False
)
