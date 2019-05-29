from setuptools import setup

setup(name='water api',
      version='0.2',
      description='A general container of apis out of Naver, Kakao',
      url='https://github.com/harry81/naver_api',
      author='Hyunmin Choi',
      author_email='pointer81@gmail.com',
      license='MIT',
      packages=['water'],
      install_requires=[
          'bs4',
      ],
      zip_safe=False)
