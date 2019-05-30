import pathlib
from setuptools import find_packages, setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
	name = 'nanome-ligand-focus',
	packages=find_packages(exclude=("nanome",)),
	version = '0.0.1',
	license='MIT',
	description = 'Nanome Plugin to easily focus on a ligand',
	long_description = README,
    long_description_content_type = "text/markdown",
	author = 'Nanome',
	author_email = 'hello@nanome.ai',
	url = 'https://github.com/nanome-ai/plugin-ligand-focus',
	platforms="any",
	keywords = ['virtual-reality', 'chemistry', 'python', 'api', 'plugin'],
	install_requires=['nanome'],
	entry_points={"console_scripts": ["nanome-ligand-focus = nanome_ligand_focus.LigandFocus:main"]},
	classifiers=[
		'Development Status :: 3 - Alpha',

		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering :: Chemistry',

		'License :: OSI Approved :: MIT License',

		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
)