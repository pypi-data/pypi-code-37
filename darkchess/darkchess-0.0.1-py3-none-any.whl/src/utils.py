from darkchess.src.dummy_piece import Dummy
from darkchess.src.piece import Piece
import numpy as np


def clean_board():
    """
    Sets up an empty board
    """
    init_board = np.zeros((8, 8), dtype=Piece)
    for i in range(8):
        for j in range(8):
            init_board[i, j] = Dummy((i, j), None)
    return init_board
