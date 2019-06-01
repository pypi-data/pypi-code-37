import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = 'praytimes',
	packages = ['praytimes'],
	version = '2.3.2',
	license ='LGPLv3',
	description = 'Packaging of praytimes.org python library',
	long_description = long_description,
	long_description_content_type="text/markdown",
	author = 'Ali Akbar',
	author_email = 'the.apaan@gmail.com',
	url = 'https://gitlab.com/apaan/praytimes-py',
	download_url = 'https://gitlab.com/apaan/praytimes-py/-/archive/v2.3.2/praytimes-py-v2.3.2.tar.gz',
	keywords = ['prayer times',],
	
	classifiers=[
		'Development Status :: 5 - Production/Stable',

		'Intended Audience :: Developers',
		'Topic :: Religion',

		'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

		'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
)
