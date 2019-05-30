from setuptools import setup

setup(name='sortingFunctions',
      version='0.1',
      description='sorting n3',
      url='https://gitlab.propulsion-home.ch/x/conda',
      author='oliver hofmann',
      author_email='x@pri.la',
      license='MIT',
      packages=['sortingFunctions'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )
