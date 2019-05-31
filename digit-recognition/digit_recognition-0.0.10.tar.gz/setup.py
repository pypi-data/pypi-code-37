import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="digit_recognition",
    version="0.0.10",
    py_modules=['digit_recognition'],
    #package_dir={'': 'src'},
    author="Maximilian Mittenbuhler",
    author_email="max.mittenbuhler@student.uva.nl",
    description="Neural network for digit recognition",
    url="https://github.com/Mittenbuhler/Neural_Network.git",
    install_requires=['numpy', 'idx2numpy', 'urllib3', 'Pillow', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'install_network = digit_recognition:install_network',
            'digit_recognition = digit_recognition:run_gui'
        ]
    },
)

# 'numpy', 'urllib3', , 'PIL', 'idx2numpy'