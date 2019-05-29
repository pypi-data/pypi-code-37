class Piece(object):
    """
    Base Piece which occupies every tile on the board
    """

    def __init__(self, pos, team=None):
        """
        Args:
            pos: the location of the piece on the board ((x,y))
            team: which team the piece is on ("white", "black")
        """
        self.pos = pos
        self.team = team
        self.name = self.get_name()
        self.value = self.get_value()
        self.symbol = self.get_symbol()
        self.moved = False

    def get_position(self):
        """
        Returns position of Piece on the board
        """
        return self.pos

    def get_team(self):
        """
        Returns which team the piece belongs to on the board
        """
        return self.team

    def get_name(self):
        """
        Returns name of the Piece
        """
        raise NotImplementedError("must be implemented")

    def get_moves(self, game_states):
        """
        All possible moves for this Piece
        Args:
            game_states: list of numpy array of dtype Piece - each element is a board
        Returns list of moves (start_pos,end_pos,type_move)
        """
        raise NotImplementedError("must be implemented")

    def get_value(self):
        """
        Returns value of the Piece
        """
        raise NotImplementedError("must be implemented")

    def get_symbol(self):
        """
        Returns symbol used to represent the Piece on the board
        """
        raise NotImplementedError("must be implemented")

    def set_position(self, pos):
        """
        sets the position of the Piece on the board
        Args:
            pos: position on chess board
        """
        self.pos = pos

    def copy(self):
        """
        Returns copy of Piece (pass by value not reference)
        """
        new_piece = Piece(self.pos, self.team)
        new_piece.moved = self.moved
        return new_piece
