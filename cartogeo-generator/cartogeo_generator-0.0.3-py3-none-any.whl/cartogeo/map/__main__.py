import sys
import argparse
import logging
from ..coord import Coord
from ..exceptions import InvalidCoordException
from . import Map25k, Map50k, Map250k, MapMiniscale


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("coord1", metavar="coord1", type=str, help="Coordinate 1 - Top left of required area")
    parser.add_argument("coord2", metavar="coord2", type=str, help="Coordinate 2 - Bottom right of required area")
    parser.add_argument("path", metavar="path", type=str, help="Output image file path")
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
    parser.add_argument(
        "-d", "--debug",
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    args = parser.parse_args()
    logging.basicConfig(
        stream=sys.stdout,
        level=args.loglevel,
        format='%(levelname)s: %(message)s'
    )

    try:
        image = args.map.build(Coord(args.coord1), Coord(args.coord2))
    except InvalidCoordException as e:
        print("Error: " + str(e), file=sys.stderr)
        return

    image.save(args.path)


if __name__ == "__main__":
    main()
