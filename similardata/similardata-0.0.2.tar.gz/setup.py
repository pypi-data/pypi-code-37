from distutils.core import setup
import setuptools

console_scripts = """
[console_scripts]
similardata=similardata.cli:cli
"""

setup(
  name = 'similardata',
  packages = ['similardata'],
  version = '0.0.2',
  description = 'similardata',
  long_description = '',
  author = '',
  license = '',
  url = 'https://github.com/anisha22678/similardata',
  keywords = [],
  classifiers = [],
  install_requires = ['lazyme'],
  entry_points=console_scripts,
)
