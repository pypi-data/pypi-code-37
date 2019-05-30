# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages
import versioneer

setup(
    name="q2_omxware",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    install_requires=['omxware'],
    author="Sarath Swaminathan",
    author_email="Sarath.Swaminathan@ibm.com",
    description="Export -omics data from omxware",
    license='BSD-3-Clause',
    url="https://qiime2.org",
    entry_points={
        'qiime2.plugins':
        ['q2_omxware=q2_omxware.plugin_setup:plugin']
    },
    package_data={'q2_omxware': []},
    zip_safe=False,
)
