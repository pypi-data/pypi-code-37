from .map_25_or_50k import Map25Or50k
from .map import Map
from typing import Tuple, List


class Map50k(Map25Or50k):
    prefix: str                 # The prefix to the specific map data folder from the generic data folder
    box_mm: int = 20            # Width/Height of a box on the map (in millimeters)
    box_pixels: int = 200       # Width/Height of a box on the map (in pixels)
    scale: str = "1:50000"      # The name of the scale as a string
    scale_unit: int = 10        # PDF visual scale unit size

    # PDF visual scale 11 labels
    scale_labels: List[str] = ["0", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5 km"]

    # The size of the map on the PDF in boxes
    pdf_size_landscape: Tuple[float, float] = (14, 8)
    pdf_size_portrait: Tuple[float, float] = (9.5, 12)

    skip: int = 2

    def __init__(self):
        self.prefix = Map.map_data_path() + "raster-50k/"
