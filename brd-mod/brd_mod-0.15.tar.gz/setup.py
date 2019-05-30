from distutils.core import setup
setup(
  name = 'brd_mod',         # How you named your package folder (MyLib)
  packages = ['brd_mod'],   # Chose the same as "name"
  version = '0.15',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A small library containing various statistic, econometric, financial, and geospatial functions',   # Give a short description about your library
  author = 'Ben Davison',                   # Type in your name
  author_email = 'benjabee10@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/benrdavison/brd_mod',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/benrdavison/brd_mod/archive/v_015.tar.gz',    # I explain this later on
  keywords = ['statistics', 'economics', 'geospatial', 'probability', 'econometrics', 'finance'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          'statsmodels',
          'scipy',
          'matplotlib',


      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)