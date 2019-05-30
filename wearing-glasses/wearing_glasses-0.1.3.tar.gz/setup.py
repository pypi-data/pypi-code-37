import setuptools
from wearing_glasses import __version__, __author__, __email__

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'numpy',
    'Pillow',
    'dlib',
    'click',
    'random'
]

setuptools.setup(
    name="wearing_glasses",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Package for 'wearing glasses'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.ai.game.tw",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'cp_fl_model=wearing_glasses.cp_fl_model:main',
            'plot_glasses=wearing_glasses.plot_glasses:main',
            'help_wearing_glasses=wearing_glasses.helper:main',
        ]
    },    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
