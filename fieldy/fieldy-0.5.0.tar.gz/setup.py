# from distutils.core import setup
from setuptools import setup
import setuptools
setup(
  name = 'fieldy',        
  packages=setuptools.find_packages(),
  package_data = {'fieldy': ['definition/*.json']},
  version = '0.5.0',      
  license='MIT',      
  include_package_data=True,
  description = 'Lib to help structure objects from jsons',   
  author = 'arthurlpgc',                   
  author_email = 'arthurlpgc@gmail.com',      
  scripts = ['bin/fieldy'],
  url = 'https://github.com/NeverDefineUs/fieldy',   
  download_url = 'https://github.com/NeverDefineUs/fieldy/archive/0.5.0.tar.gz',    
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)