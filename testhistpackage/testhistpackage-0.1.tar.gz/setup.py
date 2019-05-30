from setuptools import setup,find_packages
with open("README.txt", "r") as fh:
    long_description = fh.read()
setup(
    name='testhistpackage',
    version='0.1',
    description='tutorial',
    url='',
    author='',
    author_email = '',
    long_description = long_description,
    long_description_content_type="text/markdown",
    license = 'MIT',
    install_requires=[
          'pandas','numpy','scipy','mpl_finance','matplotlib','statsmodels','patsy'
      ],
    packages = find_packages()
)