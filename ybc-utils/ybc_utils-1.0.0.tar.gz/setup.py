from distutils.core import setup

setup(
    name='ybc_utils',
    version='1.0.0',
    description='ybc utils package',
    long_description='include common utils, eg. image utils, font utils',
    author='lanbo',
    author_email='lanbo@fenbi.com',
    keywords=['pip3', 'python3', 'python'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_utils'],
    package_data={'ybc_utils': ['fonts/*']},
    license='MIT',
    install_requires=[
        'ybc_config',
        'ybc_exception',
        'pillow'
    ],
)
