from distutils.core import setup
setup(
  name = 'tksheet',
  packages = ['tksheet'],
  version = '1.8',
  license='MIT',
  description = 'Tkinter table / sheet widget',
  author = 'ragardner',
  author_email = 'ragardner@protonmail.com',
  url = 'https://github.com/ragardner/tksheet',
  download_url = 'https://github.com/ragardner/tksheet/archive/1.8.tar.gz',
  keywords = ['tkinter', 'table', 'widget'],
  install_requires=[],
  include_package_data=True,
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)
