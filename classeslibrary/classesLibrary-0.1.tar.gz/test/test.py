from myPackage import pythonFile


def test_fahrToKelv():
    '''
    make sure freezing is calculated correctly
    '''

    assert pythonFile.fahrToKelv(32) == 273.15, 'incorrect freezing point!'


