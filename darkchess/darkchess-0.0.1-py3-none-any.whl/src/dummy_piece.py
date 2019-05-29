from darkchess.src.piece import Piece
import numpy as np


class Dummy(Piece):
    """
    Dummy Piece to represent tiles on chess board with neither white or black pieces
    """

    def get_name(self):
        """
        Returns name of the Piece
        """
        return "dummy"

    def get_value(self):
        """
        Returns value of the Piece
        """
        return 0

    def get_symbol(self):
        """
        Returns symbol used to represent the Piece on the board
        """
        return "   "

    def get_moves(self, game_states):
        """
        All possible moves for this Piece
        Args:
            game_states: list of numpy array of dtype Piece - each element is a board
        Returns list of moves (start_pos, end_pos, type_move)
        """
        return []

    def copy(self):
        """
        Returns copy of Piece (pass by value not reference)
        """
        new_piece = Dummy(self.pos, self.team)
        return new_piece
