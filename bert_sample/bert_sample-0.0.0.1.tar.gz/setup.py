from setuptools import find_packages, setup
setup(
    name='bert_sample',
    version='0.0.0.1',
    description='bert',
    long_description=open('README.MD', 'r').read(),
    author='Terry Chan',  #
    author_email='napoler2008@gmail.com',
    url='https://www.terrychan.org',
    # packages=find_packages(),
    packages=['bert_sample'],  #
    install_requires=[
        'numpy',
        'flask',
        'tqdm',
        'Terry_toolkit',
        'pytorch_pretrained_bert',
        'torch'


    ]



    )

# python setup.py sdist
# #python setup.py install
# python setup.py sdist upload
