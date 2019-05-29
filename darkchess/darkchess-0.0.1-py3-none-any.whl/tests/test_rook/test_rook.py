import pytest
import numpy as np
from darkchess.src.board import Board
from darkchess.src.rook import Rook
from darkchess.src.gamengine import GameEngine
from darkchess.src.utils import clean_board


def test_rook_moves():
    """
    Places 16 Rooks at random positions and plays 100 games with
    random moves to test the mechanics.
    """
    num_games = 100
    num_moves = 300
    for i in range(num_games):
        print("game", i+1)
        board = clean_board()
        poss = np.random.randint(8, size=[16, 2])
        board = clean_board()
        for j in range(8):
            board[poss[j, 0], poss[j, 1]] = Rook(
                (poss[j, 0], poss[j, 1]), "white")
        for j in range(8, 16):
            board[poss[j, 0], poss[j, 1]] = Rook(
                (poss[j, 0], poss[j, 1]), "black")
        rook_board = Board(board)
        game = GameEngine(rook_board, player1="computer", player2="computer")
        for _ in range(num_moves):
            moves = game.all_moves()
            if len(moves) == 0:
                break
            rand_int = np.random.randint(len(moves))
            game.choose_move(moves[rand_int])
