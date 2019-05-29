import pytest
import numpy as np
from darkchess.src.board import Board
from darkchess.src.pawn import Pawn
from darkchess.src.gamengine import GameEngine
from darkchess.src.utils import clean_board


def no_pawns(board):
    """
    Checks if no more pawns exist on the board
    """
    for i in range(8):
        for j in range(8):
            if board[i, j].symbol[1] == 'p':
                return False
    return True


def test_pawn_moves():
    """
    Places 8 Pawns along two rows and plays 100 games with
    random moves to test the mechanics
    """
    num_games = 100
    num_moves = 300
    for i in range(num_games):
        print("game", i+1)
        board = clean_board()
        for j in range(8):
            board[1, j] = Pawn((1, j), "white")
        for j in range(8):
            board[6, j] = Pawn((6, j), "black")
        pawn_board = Board(board)
        game = GameEngine(pawn_board, player1="computer", player2="computer")
        for _ in range(num_moves):
            moves = game.all_moves()
            if len(moves) == 0 or no_pawns(game.Board.board):
                break
            rand_int = np.random.randint(len(moves))
            game.choose_move(moves[rand_int])
