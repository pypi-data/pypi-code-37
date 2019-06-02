import argparse
import sys
import tempfile
from copy import copy
from ..coord import Coord
from ..exceptions import InvalidCoordException
from ..map import Map25k, Map50k, Map250k, MapMiniscale
from . import PageOrientation, PDF


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("coord", metavar="<coord>", type=str, help="Coordinate - Top left square of required area")
    parser.add_argument("path", metavar="<path>", type=str, help="Output pdf file path")
    parser.add_argument(
        "-l", "--landscape",
        help="The outputted document should be landscape",
        action="store_const", dest="orientation", const=PageOrientation.LANDSCAPE,
        default=PageOrientation.LANDSCAPE,
    )
    parser.add_argument(
        "-p", "--portrait",
        help="The outputted document should be portrait",
        action="store_const", dest="orientation", const=PageOrientation.PORTRAIT,
    )
    parser.add_argument(
        "--25k",
        help="Use 1:25,000 map scale",
        action="store_const", dest="map", const=Map25k(),
        default=Map50k(),
    )
    parser.add_argument(
        "--50k",
        help="Use 1:50,000 map scale",
        action="store_const", dest="map", const=Map50k(),
    )
    parser.add_argument(
        "--250k",
        help="Use 1:250,000 map scale",
        action="store_const", dest="map", const=Map250k(),
    )
    parser.add_argument(
        "--miniscale",
        help="Use 1:1,000,000 map scale",
        action="store_const", dest="map", const=MapMiniscale(),
    )
    parser.add_argument("--title", help="The map title", default="")
    args = parser.parse_args()

    coord1 = Coord(args.coord)
    coord2 = copy(coord1)

    if args.orientation == PageOrientation.PORTRAIT:
        max_title = 40
        pdf_size = args.map.pdf_size_portrait
    else:
        max_title = 65
        pdf_size = args.map.pdf_size_landscape

    if len(args.title) > max_title:
        print("Error: Title of landscape document cannot be longer than", max_title, "characters", file=sys.stderr)
        return

    coord2.add_x(pdf_size[0]*args.map.pdf_size_scale)
    coord2.add_y(-(pdf_size[1]*args.map.pdf_size_scale))

    try:
        image = args.map.build(coord1, coord2)
    except InvalidCoordException as e:
        print("Error: " + str(e), file=sys.stderr)
        return

    map_image = tempfile.mkstemp(suffix=".png")[1]
    image.save(map_image)

    pdf = PDF(map_image, args.map.scale, args.map.scale_unit, args.map.scale_labels, pdf_size, args.map.box_mm,
              orientation=args.orientation, title=args.title)
    pdf.draw()
    pdf.save(args.path)


if __name__ == "__main__":
    main()
