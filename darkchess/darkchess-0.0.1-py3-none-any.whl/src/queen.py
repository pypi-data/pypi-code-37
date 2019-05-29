from darkchess.src.piece import Piece


class Queen(Piece):
    """
    Queen Piece (identical for both black and white in a normal game)
    """

    def get_name(self):
        """
        Returns name of the Piece
        """
        return "queen"

    def get_value(self):
        """
        Returns value of the Piece
        """
        return 9

    def get_symbol(self):
        """
        Returns symbol used to represent the Piece on the board
        """
        if self.team == "white":
            return 'wq '
        elif self.team == "black":
            return 'bq '
        else:
            raise ValueError("this team:"+self.team +
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
        pos = self.get_position()
        x, y = pos
        if self.team == "white":
            # rook moves
            for j in range(y+1, 8):
                if board[x, j].team == None:
                    moves.append((pos, (x, j), 'base'))
                elif board[x, j].team == "black":
                    moves.append((pos, (x, j), 'base'))
                    break
                else:
                    break
            for j in range(y-1, -1, -1):
                if board[x, j].team == None:
                    moves.append((pos, (x, j), 'base'))
                elif board[x, j].team == "black":
                    moves.append((pos, (x, j), 'base'))
                    break
                else:
                    break
            for i in range(x+1, 8):
                if board[i, y].team == None:
                    moves.append((pos, (i, y), 'base'))
                elif board[i, y].team == "black":
                    moves.append((pos, (i, y), 'base'))
                    break
                else:
                    break
            for i in range(x-1, -1, -1):
                if board[i, y].team == None:
                    moves.append((pos, (i, y), 'base'))
                elif board[i, y].team == "black":
                    moves.append((pos, (i, y), 'base'))
                    break
                else:
                    break
            # bishop moves
            for i in range(min(x, y)):
                if board[x-i-1, y-i-1].team == None:
                    moves.append((pos, (x-i-1, y-i-1), 'base'))
                elif board[x-i-1, y-i-1].team == "black":
                    moves.append((pos, (x-i-1, y-i-1), 'base'))
                    break
                else:
                    break

            for i in range(min(7-x, 7-y)):
                if board[x+i+1, y+i+1].team == None:
                    moves.append((pos, (x+i+1, y+i+1), 'base'))
                elif board[x+i+1, y+i+1].team == "black":
                    moves.append((pos, (x+i+1, y+i+1), 'base'))
                    break
                else:
                    break

            for i in range(min(x, 7-y)):
                if board[x-i-1, y+i+1].team == None:
                    moves.append((pos, (x-i-1, y+i+1), 'base'))
                elif board[x-i-1, y+i+1].team == "black":
                    moves.append((pos, (x-i-1, y+i+1), 'base'))
                    break
                else:
                    break

            for i in range(min(7-x, y)):
                if board[x+i+1, y-i-1].team == None:
                    moves.append((pos, (x+i+1, y-i-1), 'base'))
                elif board[x+i+1, y-i-1].team == "black":
                    moves.append((pos, (x+i+1, y-i-1), 'base'))
                    break
                else:
                    break
            return moves
        elif self.team == "black":
            # rook moves
            for j in range(y+1, 8):
                if board[x, j].team == None:
                    moves.append((pos, (x, j), 'base'))
                elif board[x, j].team == "white":
                    moves.append((pos, (x, j), 'base'))
                    break
                else:
                    break
            for j in range(y-1, -1, -1):
                if board[x, j].team == None:
                    moves.append((pos, (x, j), 'base'))
                elif board[x, j].team == "white":
                    moves.append((pos, (x, j), 'base'))
                    break
                else:
                    break
            for i in range(x+1, 8):
                if board[i, y].team == None:
                    moves.append((pos, (i, y), 'base'))
                elif board[i, y].team == "white":
                    moves.append((pos, (i, y), 'base'))
                    break
                else:
                    break
            for i in range(x-1, -1, -1):
                if board[i, y].team == None:
                    moves.append((pos, (i, y), 'base'))
                elif board[i, y].team == "white":
                    moves.append((pos, (i, y), 'base'))
                    break
                else:
                    break
            # bishop moves
            for i in range(min(x, y)):
                if board[x-i-1, y-i-1].team == None:
                    moves.append((pos, (x-i-1, y-i-1), 'base'))
                elif board[x-i-1, y-i-1].team == "white":
                    moves.append((pos, (x-i-1, y-i-1), 'base'))
                    break
                else:
                    break

            for i in range(min(7-x, 7-y)):
                if board[x+i+1, y+i+1].team == None:
                    moves.append((pos, (x+i+1, y+i+1), 'base'))
                elif board[x+i+1, y+i+1].team == "white":
                    moves.append((pos, (x+i+1, y+i+1), 'base'))
                    break
                else:
                    break

            for i in range(min(x, 7-y)):
                if board[x-i-1, y+i+1].team == None:
                    moves.append((pos, (x-i-1, y+i+1), 'base'))
                elif board[x-i-1, y+i+1].team == "white":
                    moves.append((pos, (x-i-1, y+i+1), 'base'))
                    break
                else:
                    break

            for i in range(min(7-x, y)):
                if board[x+i+1, y-i-1].team == None:
                    moves.append((pos, (x+i+1, y-i-1), 'base'))
                elif board[x+i+1, y-i-1].team == "white":
                    moves.append((pos, (x+i+1, y-i-1), 'base'))
                    break
                else:
                    break
            return moves

        else:
            raise ValueError("this team:"+self.team +
                             " doesn't exist in the realm of this game")

    def copy(self):
        """
        Returns copy of Piece (pass by value not reference)
        """
        new_piece = Queen(self.pos, self.team)
        new_piece.moved = self.moved
        return new_piece
