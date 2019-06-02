from .map import Map
from .map_25_or_50k import Map25Or50k
from typing import Tuple, List


class Map25k(Map25Or50k):
    prefix: str                 # The prefix to the specific map data folder from the generic data folder
    box_mm: int = 40            # Width/Height of a box on the map (in millimeters)
    box_pixels: int = 400       # Width/Height of a box on the map (in pixels)
    scale: str = "1:25000"      # The name of the scale as a string
    scale_unit: int = 8         # PDF visual scale unit size

    # PDF visual scale 11 labels
    scale_labels: List[str] = ["0", "200", "400", "600", "800", "1000", "1200", "1400", "1600", "1800", "2000 m"]

    # The size of the map on the PDF in boxes
    pdf_size_landscape: Tuple[float, float] = (7, 4)
    pdf_size_portrait: Tuple[float, float] = (4.75, 6)

    skip: int = 1

    def __init__(self):
        self.prefix = Map.map_data_path() + "raster-25k/"
