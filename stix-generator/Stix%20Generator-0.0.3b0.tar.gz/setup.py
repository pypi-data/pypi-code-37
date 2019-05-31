from setuptools import setup, find_packages

setup(
    name='Stix Generator',
    version='0.0.3b',
    author='Darryl lane',
    author_email='DarrylLane101@gmail.com',
    url='https://github.com/darryllane/stix',
    packages=['Stix'],
    include_package_data=True,
    license='LICENSE.txt',
    description='''Build a STIX Indicator document containing a File and relevant hash''',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    scripts=['Stix/indicator_hash_creator.py'],
    install_requires=[
        "cybox",
		"argparse",
		"stix"
    ],
)