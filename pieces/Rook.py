from pieces.Piece import *

class Rook(Piece):
    """
    The Rook class represents the rook piece in the chess game, inheriting from the Piece class.
    """

    def __init__(self, position, color):
        """
        Initialize a rook piece.

        :param position: tuple, current position of the rook on the board.
        :param color: string, color of the rook ('white' or 'black').
        """
        if color == 'white':
            image_path = 'assets/images/white rook.png'
        else:
            image_path = 'assets/images/black rook.png'
        super().__init__(color, position, image_path)
        self.type = 'Rook'  # Type of the piece, in this case, 'Rook'
        self.valid_moves = []

    def update_valid_moves(self, my_player, enemy_player):
        """
        Update the valid moves for the rook based on the current game state.

        :param my_player: Player object representing the current player.
        :param enemy_player: Player object representing the opposing player.
        :return: None
        """
        moves_list = []
        for i in range(4):  # down, up, right, left
            path = True
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            else:
                x = -1
                y = 0
            while path:
                position_checked = (self.position[0] + (chain * x), self.position[1] + (chain * y))
                print(f"checking position :{position_checked}")
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
                if my_player.check_check(enemy_player, self.position, position_checked):
                    print(f"after this move : {position_checked} the king is in check")
        moves_list = eliminate_off_board(moves_list)
        self.valid_moves = moves_list