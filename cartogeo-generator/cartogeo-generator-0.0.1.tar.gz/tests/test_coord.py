import unittest
from cartogeo.coord import Coord
from cartogeo.exceptions import InvalidCoordException


class TestCoord(unittest.TestCase):
    _coord_letter_a = ["H", "N", "O", "S", "T"]
    _coord_letter_b = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                       "U", "V", "W", "X", "Y", "Z"]

    @staticmethod
    def _test_invalid_coord(coord: str) -> bool:
        try:
            Coord(coord)
        except InvalidCoordException:
            return False
        return True

    def test_invalid_coord_too_long(self):
        assert not self._test_invalid_coord("NG500500")

    def test_invalid_coord_too_short(self):
        assert not self._test_invalid_coord("NG55")

    def test_invalid_coord_malformed_sheet(self):
        assert not self._test_invalid_coord("005050")

    def test_invalid_coord_malformed_poing(self):
        assert not self._test_invalid_coord("NG5A5A")

    def test_invalid_sheet_name(self):
        assert not self._test_invalid_coord("NI5050")

    def test_valid_coord_correct_length(self):
        assert self._test_invalid_coord("NG5050")

    def test_valid_sheet_names(self):
        """
        Test all valid sheet names
        """
        for a in self._coord_letter_a:
            for b in self._coord_letter_b:
                sheet_name = a + b
                coord = sheet_name + "0000"
                if not self._test_invalid_coord(coord):
                    assert False
        assert True


if __name__ == "__main__":
    unittest.main()
