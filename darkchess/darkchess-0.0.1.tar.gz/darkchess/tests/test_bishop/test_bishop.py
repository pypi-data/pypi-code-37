import pytest
import numpy as np
from darkchess.src.board import Board
from darkchess.src.bishop import Bishop
from darkchess.src.gamengine import GameEngine
from darkchess.src.utils import clean_board


def test_bishop_moves():
    """
    Places 8 Bishops along two rows and plays 100 games with
    random moves to test the mechanics.
    """
    num_games = 100
    num_moves = 300
    for i in range(num_games):
        print("game", i+1)
        board = clean_board()
        for j in range(8):
            board[1, j] = Bishop((1, j), "white")
        for j in range(8):
            board[6, j] = Bishop((6, j), "black")
        bishop_board = Board(board)
        game = GameEngine(bishop_board, player1="computer", player2="computer")
        for _ in range(num_moves):
            moves = game.all_moves()
            if len(moves) == 0:
                break
            rand_int = np.random.randint(len(moves))
            game.choose_move(moves[rand_int])
