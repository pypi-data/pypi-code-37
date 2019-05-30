from setuptools import setup

setup(name='yourai',
      version='0.0.4',
      description="The CLI for the annotation tool for yourai",
      url='',
      author='Kevin Lu',
      author_email='kevin@yourai.io',
      license='Apache License Version 2.0',
      packages=['yourai'],
      install_requires=[
            'Click>=7.0',
            'flask>=1.0.3'
      ],
      entry_points={
            "console_scripts": ["yourai = yourai.cli:main"]
      }
      ,
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
