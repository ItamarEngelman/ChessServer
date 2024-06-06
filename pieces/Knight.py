from pieces.Piece import *

class Knight(Piece):
    """
    The Knight class represents the knight piece in the chess game, inheriting from the Piece class.
    """

    def __init__(self, position, color):
        """
        Initialize a knight piece.

        :param position: tuple, current position of the knight on the board.
        :param color: string, color of the knight ('white' or 'black').
        """
        image_path = 'assets/images/white knight.png' if color == 'white' else 'assets/images/black knight.png'
        super().__init__(color, position, image_path)
        self.type = 'Knight'  # Type of the piece, in this case, 'Knight'
        self.initialize_valid_moves()

    def initialize_valid_moves(self):
        """
        Initialize the initial valid moves for the knight based on its position and color.

        :return: None
        """
        offset = 1 if self.color == 'white' else -1
        self.valid_moves = [(self.position[0] + 1, self.position[1] + 2 * offset),
                            (self.position[0] - 1, self.position[1] + 2 * offset)]
        self.valid_moves = eliminate_off_board(self.valid_moves)

    def update_valid_moves(self, my_player, enemy_player):
        """
        Update the valid moves for the knight based on the current game state.

        :param my_player: Player object representing the current player.
        :param enemy_player: Player object representing the opposing player.
        :return: None
        """
        moves_list = []
        # 8 squares to check for knights, they can go two squares in one direction and one in another
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            target = (self.position[0] + targets[i][0], self.position[1] + targets[i][1])
            if target not in my_player.get_all_positions() and not my_player.check_check(enemy_player, self.position, target):
                moves_list.append(target)
        moves_list = eliminate_off_board(moves_list)
        self.valid_moves = moves_list
