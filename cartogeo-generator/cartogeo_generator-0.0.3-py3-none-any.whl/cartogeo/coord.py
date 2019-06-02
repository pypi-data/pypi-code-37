import operator
import math
from .helper import Helper
from .exceptions import InvalidCoordException, InvalidSheetException
from typing import Tuple


class Coord:
    sheet_name: str = None
    sheet_tuple: Tuple[int, int] = None
    x: int = 0
    xs: int = 0
    y: int = 0
    ys: int = 0

    _sheet_a_letter_switcher = {
        "H": (0, 0),
        "N": (0, 5),
        "O": (5, 5),
        "S": (0, 10),
        "T": (5, 10),
    }
    _sheet_a_tuple_switcher = {
        (0, 0): "H",
        (0, 5): "N",
        (5, 5): "O",
        (0, 10): "S",
        (5, 10): "T",
    }
    _sheet_b_letter_switcher = {
        "A": (0, 0),
        "B": (1, 0),
        "C": (2, 0),
        "D": (3, 0),
        "E": (4, 0),
        "F": (0, 1),
        "G": (1, 1),
        "H": (2, 1),
        "J": (3, 1),
        "K": (4, 1),
        "L": (0, 2),
        "M": (1, 2),
        "N": (2, 2),
        "O": (3, 2),
        "P": (4, 2),
        "Q": (0, 3),
        "R": (1, 3),
        "S": (2, 3),
        "T": (3, 3),
        "U": (4, 3),
        "V": (0, 4),
        "W": (1, 4),
        "X": (2, 4),
        "Y": (3, 4),
        "Z": (4, 4),
    }
    _sheet_b_tuple_switcher = {
        (0, 0): "A",
        (1, 0): "B",
        (2, 0): "C",
        (3, 0): "D",
        (4, 0): "E",
        (0, 1): "F",
        (1, 1): "G",
        (2, 1): "H",
        (3, 1): "J",
        (4, 1): "K",
        (0, 2): "L",
        (1, 2): "M",
        (2, 2): "N",
        (3, 2): "O",
        (4, 2): "P",
        (0, 3): "Q",
        (1, 3): "R",
        (2, 3): "S",
        (3, 3): "T",
        (4, 3): "U",
        (0, 4): "V",
        (1, 4): "W",
        (2, 4): "X",
        (3, 4): "Y",
        (4, 4): "Z",
    }

    def __init__(self, coord: str = None) -> None:
        super().__init__()
        if len(coord) == 6:
            try:
                self.x = int(coord[2:4])
                self.y = int(coord[4:6])
            except ValueError:
                raise InvalidCoordException("Characters 3 to 6 of a coord should be numbers")
        elif len(coord) == 8:
            try:
                self.x = int(coord[2:4])
                self.xs = int(coord[4])
                self.y = int(coord[5:7])
                self.ys = int(coord[7])
            except ValueError:
                raise InvalidCoordException("Characters 3 to 8 of a coord should be numbers")
        else:
            raise InvalidCoordException("Coord should be 6 or 8 characters long")
        self.sheet_name = coord[0:2]
        self.sheet_tuple = self.sheet_to_tuple(self.sheet_name)

    @staticmethod
    def tuple_to_sheet(sheet_tuple: Tuple[int, int]) -> str:
        sheet_a = Helper.round_down(sheet_tuple[0], 5), Helper.round_down(sheet_tuple[1], 5)
        sheet_b = tuple(map(operator.mod, sheet_tuple, (5, 5)))
        sheet_a_letter = Coord._sheet_a_tuple_switcher.get(sheet_a)
        sheet_b_letter = Coord._sheet_b_tuple_switcher.get(sheet_b)
        if sheet_a_letter is None or sheet_b_letter is None:
            raise InvalidSheetException()
        return sheet_a_letter + sheet_b_letter

    @staticmethod
    def sheet_to_tuple(sheet_name: str) -> Tuple[int, int]:
        sheet_a = Coord._sheet_a_letter_switcher.get(sheet_name[0])
        sheet_b = Coord._sheet_b_letter_switcher.get(sheet_name[1])
        if sheet_a is None or sheet_b is None:
            raise InvalidCoordException("'" + sheet_name + "' is not a valid map sheet")
        return sheet_a[0] + sheet_b[0], sheet_a[1] + sheet_b[1]

    @staticmethod
    def validate_coord_pair(coord1: 'Coord', coord2: 'Coord') -> bool:
        """
        Validates a pair of coordinates
        :param coord1:
        :param coord2:
        :return: True if valid, False if not
        """
        if coord2.sheet_tuple[0] < coord1.sheet_tuple[0]:
            return False
        if coord2.sheet_tuple[1] < coord1.sheet_tuple[1]:
            return False
        if coord1.sheet_tuple[0] == coord2.sheet_tuple[0]:
            if coord1.x > coord2.x:
                return False
        if coord1.sheet_tuple[1] == coord2.sheet_tuple[1]:
            if coord1.y < coord2.y:
                return False
        return True

    def add_x(self, x: int):
        self.x = self.x + x
        if self.x < 0 or self.x > 99:
            a = self.x % 100
            b = math.floor(self.x / 100)
            self.x = a
            self.sheet_tuple = (self.sheet_tuple[0] + b, self.sheet_tuple[1])
            self.sheet_name = self.tuple_to_sheet(self.sheet_tuple)

    def add_y(self, y: int):
        self.y = self.y + y
        if self.y < 0 or self.y > 99:
            a = self.y % 100
            b = math.floor(self.y / 100)
            self.y = a
            self.sheet_tuple = (self.sheet_tuple[0], self.sheet_tuple[1] - b)
            self.sheet_name = self.tuple_to_sheet(self.sheet_tuple)

    def __str__(self) -> str:
        return "{0}{1:02}{2}{3:02}{4}".format(self.sheet_name, self.x, self.xs, self.y, self.ys)
