from distutils.core import setup
setup(
  name = 'spychronous',
  packages = ['spychronous'],
  version = '1.0.post1',
  license='MIT',
  description = 'A simple synchronous job runner for parallel processing tasks in Python.',
  author = 'Santiago C Paredes',
  author_email = 'santiago.paredes2012@gmail.com',
  url = 'https://github.com/scparedes/spychronous',
  download_url = 'https://github.com/scparedes/spychronous/archive/v1.0.tar.gz',
  keywords = ['multiprocessing', 'multiprocess', 'multi', 'process', 'synchronous', 'job', 'runner'],
  install_requires=[
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
  ],
)