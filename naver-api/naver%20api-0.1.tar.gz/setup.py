from setuptools import setup

setup(name='naver api',
      version='0.1',
      description='The naver api joke in the world',
      url='https://github.com/harry81/naver_api',
      author='Hyunmin Choi',
      author_email='pointer81@gmail.com',
      license='MIT',
      packages=['naver_api'],
      install_requires=[
          'bs4',
      ],
      zip_safe=False)
