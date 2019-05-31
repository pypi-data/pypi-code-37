import setuptools

requires = [
    'pandas==0.24.2',
    'lxml==4.3.3']

setuptools.setup(
    name="dsd_elections",
    version="0.1.0",
    description="Scrape and package election data from Wikipedia.",
    author="Robin Linderborg",
    author_email="robin@datastory.org",
    install_requires=requires,
    packages=setuptools.find_packages()
)
