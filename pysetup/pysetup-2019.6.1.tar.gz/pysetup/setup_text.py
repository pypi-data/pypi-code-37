setup_text = '''\
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Detail see: https://packaging.python.org/tutorials/packaging-projects/#creating-setup-pypip install -i https://test.pypi.org/simple/ pysetup
setuptools.setup(
    name='<package_name>',
    version='<version>',
    author='<author>',
    author_email='<author_email>',
    description='<description>',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='<url>',
    packages=setuptools.find_packages(exclude=['<directory_name>']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['<package_name>'],
    entry_points={
        'console_scripts': ['<command>=<package>.<filename>:<function>'],
    },
)
'''
