import numpy as np
from typing import Tuple, List
from . import Map
from ..coord import Coord
from ..helper import Helper


class Map25Or50k(Map):
    prefix: str                 # The prefix to the specific map data folder from the generic data folder
    box_mm: int                 # Width/Height of a box on the map (in millimeters)
    box_pixels: int             # Width/Height of a box on the map (in pixels)
    scale: str                  # The name of the scale as a string
    scale_unit: int             # PDF visual scale unit size
    scale_labels: List[str]     # PDF visual scale 11 labels

    # The size of the map on the PDF in boxes
    pdf_size_landscape: Tuple[float, float]
    pdf_size_portrait: Tuple[float, float]

    skip: int

    def build_sources(self, coord1: Coord, coord2: Coord, extension: str = "tif") -> list:
        """
        Builds a 2D array of source images that should be used to construct the map
        :param coord1: Top left coord
        :param coord2: Bottom right coord
        :param extension: File extension
        :return: A 2D array of source images
        """
        output = []
        for y in range(coord2.sheet_tuple[1], coord1.sheet_tuple[1] - 1, -1):
            for j in range(0, 10, self.skip):
                if y == coord1.sheet_tuple[1] and j > int(Helper.round_down(coord1.y + 1, self.skip * 10) / 10):
                    continue
                if y == coord2.sheet_tuple[1] and j < int(Helper.round_down(coord2.y, self.skip * 10) / 10):
                    continue
                row = []
                for x in range(coord1.sheet_tuple[0], coord2.sheet_tuple[0] + 1):
                    for i in range(0, 10, self.skip):
                        if x == coord1.sheet_tuple[0] and i < int(Helper.round_down(coord1.x, self.skip * 10) / 10):
                            continue
                        if x == coord2.sheet_tuple[0] and i > int(Helper.round_down(coord2.x - 1, self.skip * 10) / 10):
                            continue
                        sheet_name = Coord.tuple_to_sheet((x, y)).lower()
                        path = sheet_name + "/" + sheet_name + str(i) + str(j) + "." + extension
                        row.append(path)
                output.insert(0, row)
        return output

    def calculate_crop(self, coord1: Coord, coord2: Coord) -> Tuple[float, float, float, float]:
        source_size = self.skip * 10
        x1 = int(Helper.round_down(coord1.x, source_size))
        x2 = int(Helper.round_down(coord2.x - 1, source_size))
        y1 = int(Helper.round_down(coord1.y + 1, source_size))
        y2 = int(Helper.round_down(coord2.y, source_size))

        t1 = x1, y1 + source_size - 1
        t2 = x2 + source_size - 1, y2

        left = coord1.x - t1[0] + (coord1.xs / 10)
        top = t1[1] - coord1.y + 1 - (coord1.ys / 10)
        right = t2[0] - coord2.x + 1 - (coord2.xs / 10)
        bottom = coord2.y - t2[1] + (coord2.ys / 10)

        return left, top, right, bottom

    def crop(self, structure: np.array, coord1: Coord, coord2: Coord) -> np.array:
        """
        Crop the structure which contains all of the source imagery to only contain the requested area
        :param structure: Uncropped numpy image structure
        :param coord1: Top left coord
        :param coord2: Bottom right coord
        :return: Cropped numpy image structure
        """
        left, top, right, bottom = self.calculate_crop(coord1, coord2)
        return self._crop_boxes(structure, left, top, right, bottom)
