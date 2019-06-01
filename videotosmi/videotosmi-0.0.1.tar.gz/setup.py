from setuptools import setup, find_packages

setup(name='videotosmi',
      version='0.0.1',
      url='https://github.com/Sotaneum/VideoToSMI',
      license='MIT',
      author='Donggun LEE',
      author_email='gnyotnu39@gmail.com',
      description='Create a smi file based on the video.',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False,
      setup_requires=['deepgeo==0.0.1','scipy','opencv-python','matplotlib'])