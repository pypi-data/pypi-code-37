import pytest
from darkchess.src.board import Board
from darkchess.src.pawn import Pawn
from darkchess.src.gamengine import GameEngine
from darkchess.src.utils import clean_board


def test_enpasse():
    """
    checks if white and black pawns can do enpasse
    """
    board = clean_board()
    board[3, 2] = Pawn((3, 2), "white")
    board[6, 1] = Pawn((6, 1), "black")
    board[3, 4] = Pawn((3, 4), "black")
    board[1, 5] = Pawn((1, 5), "white")
    pawn_board = Board(board)
    game = GameEngine(pawn_board, player1="computer", player2="computer")
    moves = game.all_moves()
    game.choose_move(moves[1])
    moves = game.all_moves()
    game.choose_move(moves[1])
    moves = game.all_moves()
    game.choose_move(moves[0])
    moves = game.all_moves()
    game.choose_move(moves[2])
    moves = game.all_moves()
    game.choose_move(moves[1])
