import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timetime",
    version="0.1",
    author="Robert Sebille",
    author_email="robert@sebille.name",
    maintainer = 'Robert Sebille',
    maintainer_email = 'robert@sebille.name',
    description="timetime est un micromodule de comparaison de temps\
 d'exécution de 2 ou 3 fonctions sans argument.",
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
