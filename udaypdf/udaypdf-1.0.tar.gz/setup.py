import setuptools
from pathlib import Path
setuptools.setup(
    name = "udaypdf",
    version = 1.0,
    longdescription=Path("README.MD").read_text(),
    packages = setuptools.find_packages(exclude=["tests","data"])
)