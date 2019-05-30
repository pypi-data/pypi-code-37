from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='my_sorting_algorithms_gioxon',
      version='0.1',
      description='Basic algorithms for sorting numbers',
      url='https://gitlab.propulsion-home.ch/gioxon/week-3/tree/day4_/day4/my_sorting_algorithms',
      author='Gio Xon',
      author_email='giorgo.xonikis@gmail.com',
      license='MIT',
      packages=['my_sorting_algorithms'],
      zip_safe=False)