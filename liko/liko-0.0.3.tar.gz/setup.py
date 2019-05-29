from setuptools import setup

# Used in pypi.org as the README description of your package
with open("README.md", 'r') as f:
    long_description = f.read()

setup(
        name='liko', 
        version='0.0.3',
        description='learning today make you better tomorrow',
        author='eko',
        author_email='eko@altoshift.com',
        license="MIT",
        url="https://altoshift.com",
        packages=['liko'],
        #scripts=['scripts/some_script.py'],
        #python_requires='>=3',
        requires=[],
        install_requires=[
            'pandas',
            'multiprocessing'
        ],
        long_description=long_description
)