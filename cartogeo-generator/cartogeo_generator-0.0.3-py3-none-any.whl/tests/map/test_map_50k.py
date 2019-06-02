import unittest
from mock import patch, MagicMock
from cartogeo.map.map_50k import Map50k
from cartogeo.coord import Coord
import numpy as np


class TestMap50k(unittest.TestCase):

    def test_build_sources_1(self):
        sources = Map50k().build_sources(Coord("NH9506"), Coord("NO1090"))
        assert sources == [['nh/nh80.tif', 'nj/nj00.tif'], ['nn/nn88.tif', 'no/no08.tif']]

    def test_build_sources_2(self):
        sources = Map50k().build_sources(Coord("NH0127"), Coord("NH1420"))
        assert sources == [['nh/nh02.tif']]

    @staticmethod
    def _test_build_structure(mock_imread: MagicMock, coord1: Coord, coord2: Coord, shape1: tuple, shape2: tuple):
        mock_imread.return_value = np.zeros((4000, 4000, 3))
        map50k = Map50k()
        sources = map50k.build_sources(coord1, coord2)
        structure = map50k._build_structure(sources)
        assert structure.shape == shape1
        structure = map50k.crop(structure, coord1, coord2)
        assert structure.shape == shape2

    @patch('skimage.io.imread')
    def test_build_structure_1(self, mock_imread: MagicMock):
        self._test_build_structure(
            mock_imread,
            Coord("NH9506"), Coord("NO1090"),
            (8000, 8000, 3), (3400, 3200, 3)
        )

    @patch('skimage.io.imread')
    def test_build_structure_2(self, mock_imread: MagicMock):
        self._test_build_structure(
            mock_imread,
            Coord("NH0127"), Coord("NH1420"),
            (4000, 4000, 3), (1600, 2800, 3)
        )


if __name__ == "__main__":
    unittest.main()
