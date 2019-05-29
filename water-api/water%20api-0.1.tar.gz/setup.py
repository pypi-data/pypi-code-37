from setuptools import setup

setup(name='water api',
      version='0.1',
      description='A general container of apis',
      url='https://github.com/harry81/naver_api',
      author='Hyunmin Choi',
      author_email='pointer81@gmail.com',
      license='MIT',
      packages=['water'],
      install_requires=[
          'bs4',
      ],
      zip_safe=False)
