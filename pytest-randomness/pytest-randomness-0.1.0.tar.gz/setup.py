from setuptools import setup

setup(
    name='pytest-randomness',
    version='0.1.0',
    author='Maks3w',
    license='MIT',
    url='https://github.com/Maks3w/pytest-randomness',
    description='Pytest plugin about random seed management',
    py_modules=['pytest_randomness'],
    install_requires=['pytest>=2.8'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'pytest_randomness = pytest_randomness',
        ],
    },
)
