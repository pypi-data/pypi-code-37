from setuptools import setup, find_packages

setup(name='ConfigHelper',
      version='0.0.3',
      url='https://github.com/Sotaneum/ConfigHelper',
      author='Donggun LEE',
      author_email='gnyotnu39@gmail.com',
      description='Can use it to save or recall preferences from Python.',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False,
      classifiers=[
          'License :: OSI Approved :: MIT License'
      ]
)
