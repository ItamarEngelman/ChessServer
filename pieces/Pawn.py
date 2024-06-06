from pieces.Queen import *
from pieces.Rook import *
from pieces.Bishop import *
from pieces.Knight import *
from pieces.Piece import *


class Pawn(Piece):
    """
    פעולה המייצגת אוביקטים מסוג פון. יורשת , כמו שאר החתיכות, ממחלקת חתיכה. מקבל את מיקום התמונה, את מיקום החייל והאם הפון זז או לא. הסוג הופך אוטומטית לסוג של פון. כמו כן , מקבל את הצבע של הפון.
    """
    color_promotion = ''

    def __init__(self, position, color):
        """A function to initialize a pawn piece

        Args:
            position (tuple): current position of the pawn on the board
            color (string): color of the pawn ('white' or 'black')
        """
        image_path = 'assets/images/white pawn.png' if color == 'white' else 'assets/images/black pawn.png'
        super().__init__(color, position, image_path)
        self.since_moved = 0
        self.type = 'Pawn'
        self.initialize_valid_moves()

    def initialize_valid_moves(self):
        """Initialize the initial valid moves for the pawn based on its position and color."""
        offset = 1 if self.color == 'white' else -1
        self.valid_moves = (
        [(self.position[0], self.position[1] + offset), (self.position[0], self.position[1] + 2 * offset)], [])
        self.valid_moves = (eliminate_off_board(self.valid_moves[0]), self.valid_moves[1])

    def update_position(self, new_position):
        self.position = new_position
        self.since_moved = 0


    def update_since_moved(self):
        self.since_moved += 1

    def update_valid_moves(self, my_player, enemy_player):
        """
        Update the valid_moves characteristic.

        :param my_player: Player object representing the current player.
        :param enemy_player: Player object representing the opposing player.
        :return: Updated valid_moves characteristic.
        """
        moves_list = []
        ep_moves_list = self.check_ep(enemy_player)

        offset = 1 if self.color == 'white' else -1

        if (self.position[0], self.position[1] + offset) not in my_player.get_all_positions() and \
                (self.position[0], self.position[1] + offset) not in enemy_player.get_all_positions() and \
                not my_player.check_check(enemy_player, self.position, (self.position[0], self.position[1] + offset)):
            moves_list.append((self.position[0], self.position[1] + offset))

            # Indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (self.position[0], self.position[1] + 2 * offset) not in my_player.get_all_positions() and \
                    (self.position[0], self.position[1] + 2 * offset) not in enemy_player.get_all_positions() \
                    and self.moved is False and \
                    not my_player.check_check(enemy_player, self.position,
                                              (self.position[0], self.position[1] + 2 * offset)):
                moves_list.append((self.position[0], self.position[1] + 2 * offset))

        if (self.position[0] + 1, self.position[1] + offset) in enemy_player.get_all_positions() \
                and not my_player.check_check(enemy_player, self.position,
                                              (self.position[0] + 1, self.position[1] + offset)):
            moves_list.append((self.position[0] + 1, self.position[1] + offset))

        if (self.position[0] - 1, self.position[1] + offset) in enemy_player.get_all_positions() \
                and not my_player.check_check(enemy_player, self.position,
                                              (self.position[0] - 1, self.position[1] + offset)):
            moves_list.append((self.position[0] - 1, self.position[1] + offset))

        moves_list = eliminate_off_board(moves_list)
        self.valid_moves = (moves_list, ep_moves_list)

    def check_ep(self, enemy_player):
        """
        Check for en passant moves.

        :param enemy_player: Player object representing the opposing player.
        :return: List of en passant moves possible for this pawn.
        """
        ep_moves_list = []
        position_offset, new_position_offset = (4, 1) if self.color == 'white' else (3, -1)

        for piece in enemy_player.pieces:
            if piece.type == "Pawn" and piece.position[1] == position_offset and piece.since_moved == 0 \
                    and abs(self.position[0] - piece.position[0]) == 1 and self.position[1] - piece.position[1] == 0:
                ep_moves_list.append((piece.position[0], piece.position[1] + new_position_offset))

        ep_moves_list = eliminate_off_board(ep_moves_list)
        return ep_moves_list

    def check_promotion(self):
        """
        Check if the pawn has reached the end of the board for promotion.

        :return: True if the pawn is at the end of the board, False otherwise.
        """
        offset = 7 if self.color == 'white' else 0
        if self.position[1] == offset:
            Pawn.color_promotion = self.color
            return True
        return False

    def promotion(self, new_type):
        """
        Promote the pawn to a new piece.

        :param new_type: Name of the new piece type.
        :return: An object of the new type chosen, or None if the type is unknown.
        """
        Pawn.color_promotion = self.color
        if self.color == 'white':
            if new_type == "Queen":
                return Queen(self.position, self.color)
            if new_type == "Rook":
                return Rook(self.position, self.color)
            if new_type == "Bishop":
                return Bishop(self.position, self.color)
            if new_type == "Knight":
                return Knight(self.position, self.color)
            print(f"Error occurred - problematic type for promotion: {new_type}")
        else:
            if new_type == "Queen":
                return Queen(self.position, self.color)
            if new_type == "Rook":
                return Rook(self.position, self.color)
            if new_type == "Bishop":
                return Bishop(self.position, self.color)
            if new_type == "Knight":
                return Knight(self.position, self.color)
            print(f"Error occurred - problematic type for promotion: {new_type}")
        return None
