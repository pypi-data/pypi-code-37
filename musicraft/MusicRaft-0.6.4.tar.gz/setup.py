"""
MusicRaft
"""

#from distutils.core import setup
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(name = 'MusicRaft',
    version = '0.6.4',
    description='GUI for abcplus music notation.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/papahippo/MusicRaft',
    author = "Larry Myerscough",
    author_email='hippostech@gmail.com',
    packages=['musicraft', 'musicraft.abcraft', 'musicraft.freqraft', 'musicraft.pyraft', 'musicraft.raft', 'musicraft.share', ],
    scripts=['bin/run_musicraft.py'],
    license='LICENSE.txt',
    install_requires=[
        "mido == 1.1.14",
        #"pyqtgraph >= 0.10.0",
        "lxml",
        #"pyaudio",
        "numpy",
        #"pillow",
        "PySide2",

    ],
)
