from setuptools import setup, find_packages

setup(name='VideoToSMI-Server',
      version='0.0.3',
      url='https://github.com/Sotaneum/VideoToSMI-Server',
      author='Donggun LEE',
      author_email='gnyotnu39@gmail.com',
      description='Create a smi file in Web based on the video',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False,
      setup_requires=['deepgeo','videotosmi','confighelper'],
      classifiers=[
          'License :: OSI Approved :: MIT License'
      ]
     )
