import setuptools
import re

# version number from the class
with open("timetime.py", "r") as ftt:
    readftt = ftt.readlines()

vers = re.compile(r'[0-9.]')
for i in readftt:
    if "Version" in i:
        version = ",".join(re.findall(vers, i))
        version = version.replace(",", "")

# Readme from the README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timetime",
    version=version,
    author="Robert Sebille",
    author_email="robert@sebille.name",
    maintainer = 'Robert Sebille',
    maintainer_email = 'robert@sebille.name',
    description="TimeTime est une classe qui permet d'afficher le temps \
d'exécution de fonctions, également de les comparer entre eux",
    license="GNU GPL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/zenjo/timetime/wikis/home",
    download_url = 'https://framagit.org/zenjo/timetime/tree/master',
    #packages=setuptools.find_packages(),
    py_modules = ['timetime', 'timetime_demo'],
    #packages = ['film'],
    #package_data={
    #    'film': ['frame/*', 'frames/*'],
    #},
    #data_files = [('frame',['frame/poursuiteic', 'frame/poursuiteci', 'frame/roflflyingmoto']),
    #              ('frames',['frames/bon00', 'frames/bon10', 'frames/bon20', 'frames/bon30'])],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    ],
)
