"""Tests JSON parsing."""
import os

import pytest

import pygaps


@pytest.mark.parsing
class TestJson():
    def test_isotherm_to_json(self, basic_isotherm):
        """Test the parsing of an isotherm to json."""

        test_isotherm_json = pygaps.isotherm_to_json(basic_isotherm)
        new_isotherm = pygaps.isotherm_from_json(test_isotherm_json)

        assert basic_isotherm == new_isotherm

    def test_pointisotherm_to_json(self, basic_pointisotherm):
        """Test the parsing of a PointIsotherm to json."""

        test_isotherm_json = pygaps.isotherm_to_json(basic_pointisotherm)
        new_isotherm = pygaps.isotherm_from_json(test_isotherm_json)

        assert basic_pointisotherm == new_isotherm

    def test_modelisotherm_to_json(self, basic_modelisotherm):
        """Test the parsing of an ModelIsotherm to json."""

        test_isotherm_json = pygaps.isotherm_to_json(basic_modelisotherm)
        new_isotherm = pygaps.isotherm_from_json(test_isotherm_json)

        assert basic_modelisotherm.to_dict() == new_isotherm.to_dict()

    def test_isotherm_from_json_file(self, basic_pointisotherm, tmpdir_factory):
        """Test the parsing of an isotherm to a json file."""

        path = tmpdir_factory.mktemp('json').join('isotherm.json').strpath
        pygaps.isotherm_to_jsonf(basic_pointisotherm, path)
        isotherm = pygaps.isotherm_from_jsonf(path)

        assert isotherm == basic_pointisotherm

    def test_isotherm_from_json_nist(self):
        """Test the parsing of an isotherm from json."""

        JSON_PATH_NIST = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'docs', 'examples', 'data', 'parsing', 'nist', 'nist_iso.json')

        with open(JSON_PATH_NIST) as file:
            pygaps.isotherm_from_json(file.read(), fmt='NIST')
