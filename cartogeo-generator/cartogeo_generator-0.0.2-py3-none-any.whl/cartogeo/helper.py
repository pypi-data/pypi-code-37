import math


class Helper:

    @staticmethod
    def round_down(x: int, y: int) -> int:
        return int(y * math.floor(x / y))
