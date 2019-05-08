# Copyright © 2018-2019 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Build script for setuptools"""

import setuptools

from ajsonapi import __version__

with open("README.md", "r") as fh:
    # pylint: disable=invalid-name
    long_description = fh.read()

setuptools.setup(
    name="ajsonapi",
    version=__version__,
    author="Roel van der Goot",
    author_email="roel@simplecuriosities.com",
    description="Asynchronous JSON API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rvdg/ajsonapi",
    packages=setuptools.find_packages(),
    install_requires=['asyncio', 'aiohttp', 'asyncpg', 'toposort'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
