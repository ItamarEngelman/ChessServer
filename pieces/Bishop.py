from pieces.Piece import *

class Bishop(Piece):
    """
    The Bishop class represents the bishop piece in the chess game, inheriting from the Piece class.
    """

    def __init__(self, position, color):
        """
        Initialize a bishop piece.

        :param position: tuple, current position of the bishop on the board.
        :param color: string, color of the bishop ('white' or 'black').
        """
        if color == 'white':
            image_path = 'assets/images/white bishop.png'
        else:
            image_path = 'assets/images/black bishop.png'
        super().__init__(color, position, image_path)
        self.type = 'Bishop'  # Type of the piece, in this case, 'Bishop'
        self.valid_moves = []

    def update_valid_moves(self, my_player, enemy_player):
        """
        Update the valid moves for the bishop based on the current game state.

        :param my_player: Player object representing the current player.
        :param enemy_player: Player object representing the opposing player.
        :return: None
        """
        moves_list = []
        for i in range(4):  # up-right, up-left, down-right, down-left
            path = True
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            else:
                x = -1
                y = 1
            while path:
                position_checked = (self.position[0] + (chain * x), self.position[1] + (chain * y))
                if not InBoard(position_checked):
                    path = False
                elif position_checked not in my_player.get_all_positions():
                    if not my_player.check_check(enemy_player, self.position, position_checked):
                        moves_list.append(position_checked)
                    if position_checked in enemy_player.get_all_positions():
                        path = False
                    chain += 1
                else:
                    path = False
        moves_list = eliminate_off_board(moves_list)
        self.valid_moves = moves_list
