from darkchess.src.board import Board
from sty import fg, bg, rs


class DarkBoard(Board):
    """
    Layout of the game and pieces for dark mode
    """

    def __str__(self):
        """
        Represent the Chess Board the way dark mode shows them
        """
        visible_pos = self.all_pos()
        board_rep = "  A  B  C  D  E  F  G  H \n"
        for i in range(7, -1, -1):
            board_rep += str(i+1)+" "
            for j in range(0, 8, 1):
                if(i % 2 == 0 and j % 2 == 1):
                    if (i, j) in visible_pos:
                        board_rep += bg.white + fg.black + \
                            self.board[i, j].symbol + fg.rs + bg.rs
                    else:
                        board_rep += bg.white + fg.black + \
                            " u " + fg.rs + bg.rs
                if(i % 2 == 1 and j % 2 == 1):
                    if (i, j) in visible_pos:
                        board_rep += bg.black + fg.white + \
                            self.board[i, j].symbol + fg.rs + bg.rs
                    else:
                        board_rep += bg.black + fg.white + \
                            " u " + fg.rs + bg.rs
                if(i % 2 == 0 and j % 2 == 0):
                    if (i, j) in visible_pos:
                        board_rep += bg.black + fg.white + \
                            self.board[i, j].symbol + fg.rs + bg.rs
                    else:
                        board_rep += bg.black + fg.white + \
                            " u " + fg.rs + bg.rs
                if(i % 2 == 1 and j % 2 == 0):
                    if (i, j) in visible_pos:
                        board_rep += bg.white + fg.black + \
                            self.board[i, j].symbol + fg.rs + bg.rs
                    else:
                        board_rep += bg.white + fg.black + \
                            " u " + fg.rs + bg.rs

            board_rep += " "+str(i+1)
            board_rep += "\n"
        board_rep += "  A  B  C  D  E  F  G  H \n"
        return board_rep

    def all_pos(self):
        """
        all positions the team can see on the board
        """
        team = self.turn
        all_moves_team = []
        all_pos_team = []
        game_state = [Board(self.board)]
        for i in range(8):
            for j in range(8):
                if self.board[i, j].team == team:
                    all_moves_team += self.board[i, j].get_moves(game_state)
                    all_pos_team.append((i, j))
        for move in all_moves_team:
            all_pos_team.append(move[1])
        return list(set(all_pos_team))

    def view_board_true_sight(self):
        """
        Represent the Chess Board the way the User is used to playing them in normal mode
        """
        board_rep = "  A  B  C  D  E  F  G  H \n"
        for i in range(7, -1, -1):
            board_rep += str(i+1)+" "
            for j in range(0, 8, 1):
                if(i % 2 == 0 and j % 2 == 1):
                    board_rep += bg.white + fg.black + \
                        self.board[i, j].symbol + fg.rs + bg.rs
                if(i % 2 == 1 and j % 2 == 1):
                    board_rep += bg.black + fg.white + \
                        self.board[i, j].symbol + fg.rs + bg.rs
                if(i % 2 == 0 and j % 2 == 0):
                    board_rep += bg.black + fg.white + \
                        self.board[i, j].symbol + fg.rs + bg.rs
                if(i % 2 == 1 and j % 2 == 0):
                    board_rep += bg.white + fg.black + \
                        self.board[i, j].symbol + fg.rs + bg.rs

            board_rep += " "+str(i+1)
            board_rep += "\n"
        board_rep += "  A  B  C  D  E  F  G  H \n"
        print(board_rep)
