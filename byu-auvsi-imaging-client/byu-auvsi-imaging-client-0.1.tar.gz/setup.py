import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

pkgs = setuptools.find_packages()
pkgs.remove('lib.test')
pkgs.append('assets')

setuptools.setup(
     name='byu-auvsi-imaging-client',  
     version='0.1',
     scripts=['gui.py'] ,
     author="BYU AUVSI Team",
     author_email="tylerm15@gmail.com",
     description="Imaging Client GUI for manual classification",
     install_requires=['requests>=2.20.1', 'pillow>=5.3.0', 'opencv-python>=3.4.2', 'ttkthemes>=2.2.0'],
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=pkgs,
     package_data={
        '': ['*.png', '*.jpg'],
     },
     url="https://github.com/BYU-AUVSI/imaging",
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )