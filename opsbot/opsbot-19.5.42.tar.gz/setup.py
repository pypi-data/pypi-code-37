import setuptools

with open("PYPI-DESC.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opsbot",
    version="19.5.42",
    author="Diep Magik",
    author_email="diepnh@magik.vn",
    description="I'm Opsbot. I can help you create the best devops scripts.",
    long_description=long_description,
    url="https://gitlab.com/magiklab/opsbot-py",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Topic :: System :: Operating System",
        "Topic :: System :: Shells",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
          'console_scripts': ['opsbot=opsbot.opsbot:main'],
    },
    include_package_data=True
)