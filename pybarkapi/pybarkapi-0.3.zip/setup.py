from distutils.core import setup
setup(
  name = 'pybarkapi',         # How you named your package folder (MyLib)
  packages = ['pybarkapi'],   # Chose the same as "name"
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple python API for bark, a useful tool for notifying you through your smart phone.',   # Give a short description about your library
  author = 'Sean',                   # Type in your name
  author_email = '652964528@qq.com',      # Type in your E-Mail
  url = 'https://github.com/wanderersean/pybarkapi',   # Provide either the link to your github or to your website
  keywords = ['BARK', 'Python', 'Notification'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2',      #Specify which pyhton versions that you want to support, can be duplicated
  ],
  version = '0.3',      # Start with a small number and increase it with every change you make
#download_url = 'https://github.com/wanderersean/pybarkapi/archive/v0.2.tar.gz',    # I explain this later on
)