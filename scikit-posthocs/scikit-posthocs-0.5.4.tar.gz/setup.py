from setuptools import setup
from os.path import join, dirname

setup(name='scikit-posthocs',
      version='0.5.4',
      description='Statistical post-hoc analysis and outlier detection algorithms',
      long_description=open(join(dirname(__file__), 'DESCRIPTION.rst')).read(),
      url='http://github.com/maximtrp/scikit-posthocs',
      author='Maksim Terpilowski',
      author_email='maximtrp@gmail.com',
      license='BSD',
      packages=['scikit_posthocs'],
      keywords='statistics posthoc anova',
      install_requires=['numpy', 'scipy', 'statsmodels',
                        'pandas>=0.20.0', 'seaborn', 'matplotlib'],
	  classifiers=[
		'Development Status :: 5 - Production/Stable',

		'Intended Audience :: Education',
		'Intended Audience :: Information Technology',
		'Intended Audience :: Science/Research',

		'Topic :: Scientific/Engineering :: Information Analysis',
		'Topic :: Scientific/Engineering :: Mathematics',

		'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	  ],
      test_suite='tests.posthocs_suite',
      zip_safe=False)
