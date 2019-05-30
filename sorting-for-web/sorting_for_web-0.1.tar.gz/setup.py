from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='sorting_for_web',
      version='0.1',
      description='4 Sorting algorithms',
      url='',
      author='Ignas M',
      author_email='',
      license='MIT',
      packages=['sorting_package'],
      test_suite="nose.collector",
      tests_require=["nose"],
      zip_safe=False)