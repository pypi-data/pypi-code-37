import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="glcs",
    version="0.1.6",
    author="Austin Fishbaugh",
    author_email="amf2015@wildcats.unh.edu",
    description="A utility for integrating GitLab into CS courses",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['setup-course=glcs.command_line:setup_course',
                            'verify-course=glcs.command_line:verify_course',
                            'add-assignment=glcs.command_line:add_assignment',
                            'add-lab=glcs.command_line:add_lab',
                            'glcsconf=glcs.command_line:config']
    },
    install_requires=[
        'python-gitlab>=1.6.0',
        'mimir-cli',
        'pyreadline;platform_system=="Windows"',
        'flask',
        'jinja2',
        'xdg',
        'argparse',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
