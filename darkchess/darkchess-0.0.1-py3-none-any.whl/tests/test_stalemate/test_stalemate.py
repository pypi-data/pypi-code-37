import pytest
import numpy as np
from darkchess.src.board import Board
from darkchess.src.pawn import Pawn
from darkchess.src.knight import Knight
from darkchess.src.gamengine import GameEngine
from darkchess.src.utils import clean_board


def test_stalemate_3moves():
    """
    Checks if the stalemate function works when the same state is repeated 3 times
    """
    board = clean_board()
    board[3, 4] = Knight((3, 4), "white")
    board[5, 4] = Knight((5, 4), "black")
    knight_board = Board(board)
    game = GameEngine(knight_board, player1="computer", player2="computer")
    with pytest.raises(SystemExit):
        white_move1 = ((3, 4), (1, 3), 'base')
        white_move2 = ((1, 3), (3, 4), 'base')
        black_move1 = ((5, 4), (3, 3), 'base')
        black_move2 = ((3, 3), (5, 4), 'base')
        for _ in range(9):
            game.choose_move(white_move1)
            game.choose_move(black_move1)
            game.choose_move(white_move2)
            game.choose_move(black_move2)


def test_stalemate_nomoves():
    """
    Two pawns blocking each other, no more moves so stalemate check
    """
    board = clean_board()
    board[3, 4] = Pawn((3, 4), "white")
    board[5, 4] = Pawn((5, 4), "black")
    pawn_board = Board(board)
    game = GameEngine(pawn_board, player1="computer", player2="computer")
    with pytest.raises(SystemExit):
        for _ in range(2):
            moves = game.all_moves()
            if len(moves) > 0:
                game.choose_move(moves[0])
            else:
                game.choose_move([])
