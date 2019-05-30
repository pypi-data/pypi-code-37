import os.path
import setuptools

root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='emake',
    version='0.1.0',
    url='https://github.com/mohanson/emake',
    license='WTFPL',
    author='mohanson',
    author_email='mohanson@outlook.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['emake'],
)
