'''
 Copyright (c) 2014, UChicago Argonne, LLC
 See LICENSE file.
'''
from setuptools import setup, find_packages
import minixs

setup(name='minixes2',
      version=minixs.__version__,
      description='Python program to process MiniXES data from sector 20',
      long_description_content_type='text/markdown',
      author = 'Brian Mattern, John Hammonds',
      author_email = 'JPHammonds@anl.gov',
      maintainer = 'John Hammonds',
      maintainer_email = 'JPHammonds@anl.gov',
      
      url = '',
      packages = find_packages() ,
#       include_package_data=True,
      package_data = {},
      install_requires = [],
#       license = 'See LICENSE File',
      platforms = 'any',
#       scripts = ['Scripts/rsMap3D',
#                  'Scripts/rsMap3D.bat'],
      )
