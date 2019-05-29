from darkchess.src.piece import Piece
import numpy as np


class King(Piece):
    """
    King Piece (identical for all both in a normal game)
    """

    def get_name(self):
        """
        Returns name of the Piece
        """
        return "king"

    def get_value(self):
        """
        Returns value of the Piece
        """
        return np.inf

    def get_symbol(self):
        """
        Returns symbol used to represent the Piece on the board
        """
        if self.team == "white":
            return 'wK '
        elif self.team == "black":
            return 'bK '
        else:
            raise ValueError("this team:" +
                             self.team +
                             " doesn't exist in the realm of this game")

    def get_moves(self, game_states):
        """
        All possible moves for this Piece
        Args:
            game_states: list of numpy array of dtype Piece - each element is a board
        Returns list of moves (start_pos,end_pos,type_move)
        """
        board = game_states[-1].board
        moves = []
        x, y = self.get_position()
        # 8 positions
        all_opp_pos, opp_king_pos = self._all_opp_moves_minus_king(game_states)
        if self.team == "white":
            if(x+1 < 8):
                if (x+1, y) not in all_opp_pos and not self.too_close((x+1, y), opp_king_pos) and board[(x+1, y)].team is None:
                    moves.append(((x, y), (x+1, y), 'base'))
                if(y+1 < 8):
                    if (x+1, y+1) not in all_opp_pos and not self.too_close((x+1, y+1), opp_king_pos) and board[(x+1, y+1)].team is None:
                        moves.append(((x, y), (x+1, y+1), 'base'))
                    if (x, y+1) not in all_opp_pos and not self.too_close((x, y+1), opp_king_pos) and board[(x, y+1)].team is None:
                        moves.append(((x, y), (x, y+1), 'base'))
                if(y > 0):
                    if (x+1, y-1) not in all_opp_pos and not self.too_close((x+1, y-1), opp_king_pos) and board[(x+1, y-1)].team is None:
                        moves.append(((x, y), (x+1, y-1), 'base'))
                    if (x, y-1) not in all_opp_pos and not self.too_close((x, y-1), opp_king_pos) and board[(x, y-1)].team is None:
                        moves.append(((x, y), (x, y-1), 'base'))
            if(x > 0):
                if (x-1, y) not in all_opp_pos and not self.too_close((x-1, y), opp_king_pos) and board[(x-1, y)].team is None:
                    moves.append(((x, y), (x-1, y), 'base'))
                if(y+1 < 8):
                    if (x-1, y+1) not in all_opp_pos and not self.too_close((x-1, y+1), opp_king_pos) and board[(x-1, y+1)].team is None:
                        moves.append(((x, y), (x-1, y+1), 'base'))
                if(y > 0):
                    if (x-1, y-1) not in all_opp_pos and not self.too_close((x-1, y-1), opp_king_pos) and board[(x-1, y-1)].team is None:
                        moves.append(((x, y), (x-1, y-1), 'base'))

            moves += self.castle_moves(game_states)

        elif self.team == "black":
            if(x+1 < 8):
                if (x+1, y) not in all_opp_pos and not self.too_close((x+1, y), opp_king_pos) and board[(x+1, y)].team is None:
                    moves.append(((x, y), (x+1, y), 'base'))
                if(y+1 < 8):
                    if (x+1, y+1) not in all_opp_pos and not self.too_close((x+1, y+1), opp_king_pos) and board[(x+1, y+1)].team is None:
                        moves.append(((x, y), (x+1, y+1), 'base'))
                    if (x, y+1) not in all_opp_pos and not self.too_close((x, y+1), opp_king_pos) and board[(x, y+1)].team is None:
                        moves.append(((x, y), (x, y+1), 'base'))
                if(y > 0):
                    if (x+1, y-1) not in all_opp_pos and not self.too_close((x+1, y-1), opp_king_pos) and board[(x+1, y-1)].team is None:
                        moves.append(((x, y), (x+1, y-1), 'base'))
                    if (x, y-1) not in all_opp_pos and not self.too_close((x, y-1), opp_king_pos) and board[(x, y-1)].team is None:
                        moves.append(((x, y), (x, y-1), 'base'))
            if(x > 0):
                if (x-1, y) not in all_opp_pos and not self.too_close((x-1, y), opp_king_pos) and board[(x-1, y)].team is None:
                    moves.append(((x, y), (x-1, y), 'base'))
                if(y+1 < 8):
                    if (x-1, y+1) not in all_opp_pos and not self.too_close((x-1, y+1), opp_king_pos) and board[(x-1, y+1)].team is None:
                        moves.append(((x, y), (x-1, y+1), 'base'))
                if(y > 0):
                    if (x-1, y-1) not in all_opp_pos and not self.too_close((x-1, y-1), opp_king_pos) and board[(x-1, y-1)].team is None:
                        moves.append(((x, y), (x-1, y-1), 'base'))

            moves += self.castle_moves(game_states)
        else:
            raise ValueError("this team:"+self.team +
                             " doesn't exist in the realm of this game")
        return moves

    def _all_opp_moves_minus_king(self, game_states):
        """
        Returns all opponent moves except their king's moves
        Args:
            board: numpy array of dtype Piece
        """
        board = game_states[-1].board
        opp_king_pos = None
        if self.team == "white":
            team = "black"
        if self.team == "black":
            team = "white"
        all_moves_team = []
        for i in range(8):
            for j in range(8):
                if board[i, j].team == team and board[i, j].get_symbol() != team[0]+"K ":
                    all_moves_team += board[i, j].get_moves(game_states)
                if board[i, j].team == team and board[i, j].get_symbol() == team[0]+"K ":
                    opp_king_pos = (i, j)
        all_pos_team = []
        for move in all_moves_team:
            all_pos_team.append(move[1])
        return list(set(all_pos_team)), opp_king_pos

    def too_close(self, pos1, pos2):
        """
        Check if two positions are within sqrt(2) distance of each other
        Used to check if the two kings are adjacent to each other
        Args:
            pos1: position on board
            pos2: position on board
        """
        if pos1 is None or pos2 is None:
            return False
        x1, y1 = pos1
        x2, y2 = pos2
        if (x1-x2)**2 + (y1-y2)**2 <= 2:
            return True
        return False

    def copy(self):
        """
        Returns copy of Piece (pass by value not reference)
        """
        new_piece = King(self.pos, self.team)
        new_piece.moved = self.moved
        return new_piece

    def castle_moves(self, game_states):
        """
        Returns castling moves
        Args:
            board: numpy array of dtype Piece
        """
        board = game_states[-1].board
        x, y = self.get_position()  # y=4
        # 8 positions
        moves = []
        all_opp_pos, opp_king_pos = self._all_opp_moves_minus_king(game_states)
        if not self.moved and (x, y) not in all_opp_pos and not board[(x, 7)].moved and board[(x, 6)].team is None and board[(x, 5)].team is None and (x, 6) not in all_opp_pos and (x, 5) not in all_opp_pos and not self.too_close((x, 6), opp_king_pos) and not self.too_close((x, 5), opp_king_pos):
            moves.append(((x, y), (x, y+2), 'castling'))
        if not self.moved and (x, y) not in all_opp_pos and not board[(x, 0)].moved and board[(x, 1)].team is None and board[(x, 2)].team is None and (x, 1) not in all_opp_pos and (x, 2) not in all_opp_pos and not self.too_close((x, 1), opp_king_pos) and not self.too_close((x, 2), opp_king_pos):
            moves.append(((x, y), (x, y-2), 'castling'))
        return moves
