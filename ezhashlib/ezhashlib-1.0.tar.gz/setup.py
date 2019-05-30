from setuptools import setup

import os
this_directory = os.getcwd()
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='ezhashlib',
      version='1.0',
      description='Convenience wrapper around the hashlib library',
      long_description_content_type="text/markdown",
      long_description=long_description,
      url='https://github.com/joshm12345/ezhashlib',
      author='Josh Morrow',
      author_email='joshmorrow12@icloud.com',
      license='MIT',
      packages=['ezhashlib'],
      zip_safe=False)
