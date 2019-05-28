import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid >= 1.10',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_retry',
    'pyramid_tm',
    'transaction',
    'waitress',
    'Markdown',
    'PyYAML',
    'python-frontmatter',
    'pyramid-htmlmin',
    'pyramid-webpack',
    'Babel',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='flatfilecms',
    version='0.3',
    description='flat-file CMS suitable for static site',
    long_description=README + '\n\n' + CHANGES,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Anton Kasimov',
    author_email='kasimov@radium-it.ru',
    url='https://trac.radium.group/flatfilecms/',
    keywords='web pyramid pylons flat-file CMS',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = flatfilecms:main',
        ],
        'console_scripts': [
            'generate_static_site = flatfilecms.scripts.generate:main',
        ],
    },
)
