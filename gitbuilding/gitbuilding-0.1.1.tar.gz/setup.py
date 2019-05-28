 
__author__ = 'Julian Stirling'

from setuptools import setup, find_packages
import sys
if sys.version_info[0] == 2:
    sys.exit("Sorry, Python 2 is not supported")


setup(name = 'gitbuilding',
      version = '0.1.1',
      description = 'For documenting and open source hardware project with minimal effort, so you can stop writing and git building.',
      long_description = 'For documenting and open source hardware project with minimal effort, so you can stop writing and git building.',
      author = 'Julian Stirling',
      author_email = 'julian@julianstirling.co.uk',
      packages = find_packages(),
      package_data={'gitbuilding': ['static/*.*','static/Logo/*.*']},
      keywords = ['Documentation','Hardware'],
      zip_safe = True,
      url = 'https://gitlab.com/bath_open_instrumentation_group/git-building',
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6'
          ],
      install_requires=['argparse','regex','pyyaml','flask','markdown'],
      python_requires=">=3.6",
      entry_points = {'console_scripts': ['gitbuilding = gitbuilding.__main__:main']},
      )

