import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='lemity',
    version='2019.6.1',
    author='Czw',
    author_email='459749926@qq.com',
    include_package_data=True,
    description='Simple video server.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Czw96/Lemity',
    packages=setuptools.find_packages(exclude=['trash']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['flask', 'toolset'],
    entry_points={
        'console_scripts': ['lemity=lemity.main:main'],
    },
)
