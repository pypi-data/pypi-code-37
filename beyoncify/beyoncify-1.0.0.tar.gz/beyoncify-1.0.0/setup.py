from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='beyoncify',
      version='1.0.0',
      description='beyoncify',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
         'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='beyonce beyoncify',
      url='https://github.com/ebsaral/beyoncify',
      author='Emin Bugra Saral',
      author_email='eminbugrasaral@me.com',
      license='BSD',
      packages=[],
      install_requires=[],
      include_package_data=True,
      zip_safe=False,
      project_urls={
        'Documentation': 'https://github.com/ebsaral/beyoncify',
        'Funding': 'https://github.com/ebsaral/beyoncify',
        'Source': 'https://github.com/ebsaral/beyoncify',
      },
      tests_require=[],
)