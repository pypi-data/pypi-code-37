from distutils.core import setup
setup(
  name = 'APIResponse',      
  packages = ['APIResponse'], 
  version = '0.2',   
  license='MIT',    
  description = 'A Custom Response class for the APIs',   
  author = 'Ayush Aggarwal',                 
  author_email = 'ayush.aggarwal@innovaccer.com',    
  url = 'https://github.com/innovaccer/APIResponse', 
  download_url = 'https://github.com/innovaccer/APIResponse/archive/v0.1.tar.gz',    # I explain this later on
  keywords = ['python', 'flask', 'response'],
    install_requires=[ "flask",         # I get to this in a second
                 
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2.7',      #Specify which pyhton versions that you want to support

  ],
)