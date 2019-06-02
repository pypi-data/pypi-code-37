from setuptools import setup, find_packages

setup(name='cocotostphoto',
      version='0.0.1',
      url='https://github.com/Sotaneum/CocoToSTPhoto',
      license='MIT',
      author='Donggun LEE',
      author_email='gnyotnu39@gmail.com',
      description='COCO DataSet instances to STPhoto',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False,
      setup_requires=['deepgeo'],
      classifiers=[
          'License :: OSI Approved :: MIT License'
      ]
)
