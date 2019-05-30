from setuptools import setup

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='galvandi_sorting_magic2',
      version='0.1.6',
      description='Just some magic',
      url='http://github.com/galvandi',
      author='galvandi',
      author_email='galvandi@derp.com',
      license='MIT',
      packages=['galvandi_sorting_magic2'],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown',
      test_suite = 'nose.collector',
      tests_require = ['nose'],
)