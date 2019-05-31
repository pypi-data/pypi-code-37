import setuptools


setuptools.setup(
    name='game_of_life_package',
    version='0.2',
    scripts='GameOfLife',
    packages=setuptools.find_packages(),
    url='https://github.com/FabCarbonia/GameOfLifePython/blob/master/game_of_life_code.py',
    download_url='https://github.com/FabCarbonia/GameOfLifePython/archive/v_01.tar.gz',
    license='MIT',
    author='Fabio',
    author_email='famelis12@gmail.com',
    description='Game of Life implementation with many options. ',
    install_requires=[
        'pygame'
    ]
)

