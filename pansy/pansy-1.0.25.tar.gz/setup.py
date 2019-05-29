from setuptools import setup, find_packages

setup(
    name="pansy",
    version='1.0.25',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['setproctitle', 'netkit', 'pyglet', 'events'],
    url="https://github.com/dantezhu/pansy",
    license="MIT",
    author="dantezhu",
    author_email="zny2008@gmail.com",
    description="pansy",
)
