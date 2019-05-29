import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sensordroid",
    version="2.1.3.4",
    author="Tarek Moghrabi",
    author_email="moghrabi.tarek@outlook.com",
    description="Sensor Droid - Streams, in real-time, sensors and camera data directly to a client device over wireless network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Proprietary",
    url="https://sites.google.com/view/sensordroid/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
