import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='merge_lookup_pkg_chickachickaaa',
      description='A script to merge large files into one excel and then do a vlookup.',
      long_description='This is a simple example package.',
      version='1.0.0',
      url='https://github.com/chickachickaaa/merge_lookup',
      author='T. Higgins',
      author_email='thiggins4890@gmail.com',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      packages=setuptools.find_packages(),
)

