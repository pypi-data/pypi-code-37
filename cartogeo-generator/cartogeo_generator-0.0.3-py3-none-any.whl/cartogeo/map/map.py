import os
import skimage.io
import skimage.color
import numpy as np
import logging
from abc import ABC, abstractmethod
from PIL import Image
from typing import Tuple, List
from ..coord import Coord
from ..exceptions import InvalidCoordException


class Map(ABC):
    prefix: str                 # The prefix to the specific map data folder from the generic data folder
    box_mm: int                 # Width/Height of a box on the map (in millimeters)
    box_pixels: int             # Width/Height of a box on the map (in pixels)
    scale: str                  # The name of the scale as a string
    scale_unit: int             # PDF visual scale unit size
    scale_labels: List[str]     # PDF visual scale 11 labels

    # The size of the map on the PDF in boxes
    pdf_size_landscape: Tuple[float, float]
    pdf_size_portrait: Tuple[float, float]
    pdf_size_scale: int = 1     # Increase in 1 X/Y equal to increase in (1*pdf_size_scale) boxes

    def build(self, coord1: Coord, coord2: Coord) -> Image:
        """
        Build a map image for the area represented between two given coordinates
        :param coord1: Top left coord
        :param coord2: Bottom right coord
        :return: The Image
        """
        if not Coord.validate_coord_pair(coord1, coord2):
            raise InvalidCoordException("Co-ord 1 should be above and to the left of Co-ord 2")
        sources = self.build_sources(coord1, coord2)
        structure = self._build_structure(sources)
        logging.debug("Shape before crop: " + str(structure.shape))
        structure = self.crop(structure, coord1, coord2)
        logging.debug("Shape after crop: " + str(structure.shape))
        if 0 in structure.shape:
            raise InvalidCoordException("The coords given resulted in an image of 0 pixels wide or high")
        image = Image.fromarray(structure.astype('uint8'))
        return image

    @abstractmethod
    def build_sources(self, coord1: Coord, coord2: Coord, extension: str = "tif") -> list:
        """
        Builds a 2D array of source images that should be used to construct the map
        :param coord1: Top left coord
        :param coord2: Bottom right coord
        :param extension: File extension
        :return: A 2D array of source images
        """
        pass

    def _build_structure(self, sources: list) -> np.array:
        """
        Loads all of the source images and constructs a numpy array containing the images attached to each other
        :param sources: A 2D array of source images
        :return: numpy image structure
        """
        row_output = []
        for row in sources:
            column_output = []
            for path in row:
                img = skimage.io.imread(self.prefix + path, plugin='pil')
                data = img.astype(np.float64)
                column_output.append(data)
            row_output.append(np.concatenate(column_output, axis=1))
        return np.concatenate(row_output, axis=0)

    @abstractmethod
    def calculate_crop(self, coord1: Coord, coord2: Coord) -> Tuple[float, float, float, float]:
        pass

    @abstractmethod
    def crop(self, structure: np.array, coord1: Coord, coord2: Coord) -> np.array:
        """
        Crop the structure which contains all of the source imagery to only contain the requested area
        :param structure: Uncropped numpy image structure
        :param coord1: Top left coord
        :param coord2: Bottom right coord
        :return: Cropped numpy image structure
        """
        pass

    def _crop_boxes(self, structure: np.array, left: float = 0, top: float = 0, right: float = 0, bottom: float = 0):
        """
        Crop a map structure by specifying the number of boxes to crop from each edge. Uses box_pixels class variable to
        determine the size of each box to crop
        :param structure:
        :param left:
        :param top:
        :param right:
        :param bottom:
        :return: The cropped map structure
        """
        x1 = int(self.box_pixels * top)
        x2 = int(structure.shape[0] - (self.box_pixels * bottom))
        y1 = int(self.box_pixels * left)
        y2 = int(structure.shape[1] - (self.box_pixels * right))
        return structure[x1:x2, y1:y2, :]

    @staticmethod
    def map_data_path():
        return "data/" if "MAP_DATA_PATH" not in os.environ else os.environ["MAP_DATA_PATH"]
