import pytest
import numpy as np
from darkchess.src.board import Board
from darkchess.src.gamengine import GameEngine
from mock import patch


def test_normal_game():
    """
    Plays 100 games with random moves to test the mechanics
    """
    num_games = 100
    num_moves = 300
    for i in range(num_games):
        print("game", i+1)
        board = Board()
        game = GameEngine(board, player1="computer", player2="computer")
        for _ in range(num_moves):
            moves = game.all_moves()
            if len(moves) == 0:
                break
            rand_int = np.random.randint(len(moves))
            with patch('sys.exit') as exit_mock:
                game.choose_move(moves[rand_int])
                if exit_mock.called:
                    break
