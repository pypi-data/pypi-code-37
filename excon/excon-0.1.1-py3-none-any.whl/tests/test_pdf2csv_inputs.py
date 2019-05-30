"""
This is a testing module for the input of convert.pdf2csv()
"""

from excon import convert


def test_input(capsys):
    input_values = ['xxx', 'nO', 23, 'YES', 'y', 'n']

    def mock_input(s):
        return input_values.pop(0)
    convert.input = mock_input

    convert.pdf2csv()

    out, err = capsys.readouterr()

    assert out == "".join(['Please try again.\n',
                           'Please try again.\n'])
    assert err == ''
    assert convert.pdf2csv() == ('True', 'False')

