from darkchess.src.piece import Piece


class Pawn(Piece):
    """
    Pawn Piece (identical for all in a game)
    """

    def get_name(self):
        """
        Returns name of the Piece
        """
        return "pawn"

    def get_value(self):
        """
        Returns value of the Piece
        """
        return 1

    def get_symbol(self):
        """
        Returns symbol used to represent the Piece on the board
        """
        if self.team == "white":
            return 'wp '
        elif self.team == "black":
            return 'bp '
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
        pos = self.get_position()
        x, y = pos
        if self.team == "white":

            if x == 1:
                if board[x+1, y].team is None:
                    moves.append((pos, (x+1, y), 'base'))
                if board[x+2, y].team is None and board[x+1, y].team is None:
                    moves.append((pos, (x+2, y), 'base'))
                if y-1 >= 0:
                    if board[x+1, y-1].team is "black":
                        moves.append((pos, (x+1, y-1), 'base'))
                if y+1 < 8:
                    if board[x+1, y+1].team is "black":
                        moves.append((pos, (x+1, y+1), 'base'))
                return moves

            if x == 4:
                if board[x+1, y].team is None:
                    moves.append((pos, (x+1, y), 'base'))
                if y-1 >= 0:
                    if board[x+1, y-1].team is "black":
                        moves.append((pos, (x+1, y-1), 'base'))
                    if len(game_states) >= 2:
                        if board[x, y-1].symbol == "bp " and game_states[-2].board[x+2, y-1].symbol == "bp ":
                            moves.append((pos, (x+1, y-1), 'enpasse'))
                if y+1 < 8:
                    if board[x+1, y+1].team is "black":
                        moves.append((pos, (x+1, y+1), 'base'))
                    if len(game_states) >= 2:
                        if board[x, y+1].symbol == "bp " and game_states[-2].board[x+2, y+1].symbol == "bp ":
                            moves.append((pos, (x+1, y+1), 'enpasse'))
                return moves

            if x < 6 and x > 1 and x != 4:
                if board[x+1, y].team is None:
                    moves.append((pos, (x+1, y), 'base'))
                if y-1 >= 0:
                    if board[x+1, y-1].team is "black":
                        moves.append((pos, (x+1, y-1), 'base'))
                if y+1 < 8:
                    if board[x+1, y+1].team is "black":
                        moves.append((pos, (x+1, y+1), 'base'))
                return moves

            if x == 6:
                if board[x+1, y].team is None:
                    moves.append((pos, (x+1, y), 'evolve'))
                if y-1 >= 0:
                    if board[x+1, y-1].team is "black":
                        moves.append((pos, (x+1, y-1), 'evolve'))
                if y+1 < 8:
                    if board[x+1, y+1].team is "black":
                        moves.append((pos, (x+1, y+1), 'evolve'))
                return moves

            if x == 7:
                raise ValueError("something went wrong, why didnt you evolve")

        elif self.team == "black":

            if x == 6:
                if board[x-1, y].team is None:
                    moves.append((pos, (x-1, y), 'base'))
                if board[x-2, y].team is None and board[x-1, y].team is None:
                    moves.append((pos, (x-2, y), 'base'))
                if y-1 >= 0:
                    if board[x-1, y-1].team is "white":
                        moves.append((pos, (x-1, y-1), 'base'))
                if y+1 < 8:
                    if board[x-1, y+1].team is "white":
                        moves.append((pos, (x-1, y+1), 'base'))
                return moves

            if x == 3:
                if board[x-1, y].team is None:
                    moves.append((pos, (x-1, y), 'base'))
                if y-1 >= 0:
                    if board[x-1, y-1].team is "white":
                        moves.append((pos, (x-1, y-1), 'base'))
                    if len(game_states) >= 2:
                        if board[x, y-1].symbol == "wp " and game_states[-2].board[x-2, y-1].symbol == "wp ":
                            moves.append((pos, (x-1, y-1), 'enpasse'))
                if y+1 < 8:
                    if board[x-1, y+1].team is "white":
                        moves.append((pos, (x-1, y+1), 'base'))
                    if len(game_states) >= 2:
                        if board[x, y+1].symbol == "wp " and game_states[-2].board[x-2, y+1].symbol == "wp ":
                            moves.append((pos, (x-1, y+1), 'enpasse'))
                return moves

            if x > 1 and x < 6 and x != 3:
                if board[x-1, y].team is None:
                    moves.append((pos, (x-1, y), 'base'))
                if y-1 >= 0:
                    if board[x-1, y-1].team is "white":
                        moves.append((pos, (x-1, y-1), 'base'))
                if y+1 < 8:
                    if board[x-1, y+1].team is "white":
                        moves.append((pos, (x-1, y+1), 'base'))
                return moves

            if x == 1:
                if board[x-1, y].team is None:
                    moves.append((pos, (x-1, y), 'evolve'))
                if y-1 >= 0:
                    if board[x-1, y-1].team is "white":
                        moves.append((pos, (x-1, y-1), 'evolve'))
                if y + 1 < 8:
                    if board[x-1, y+1].team is "white":
                        moves.append((pos, (x-1, y+1), 'evolve'))
                return moves

            if x == 0:
                raise ValueError("something went wrong, why didnt you evolve")
        else:
            raise ValueError("this team:" +
                             self.team +
                             " doesn't exist in the realm of this game")

    def copy(self):
        """
        Returns copy of Piece (pass by value not reference)
        """
        new_piece = Pawn(self.pos, self.team)
        new_piece.moved = self.moved
        return new_piece
