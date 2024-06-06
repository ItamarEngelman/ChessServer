from pieces.King import King
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Bishop import Bishop
from pieces.Knight import Knight
from pieces.Pawn import Pawn
from utils import *

class Player():
    def __init__(self, color, pieces, capture_pieces):
        self.color = color
        self.check = False
        self.pieces = pieces
        self.capture_pieces = capture_pieces

    def get_all_positions(self):
        """
        Get all positions of the player's pieces.

        :return: List of positions of the player's pieces.
        """
        pieces_positions = []
        for piece in self.pieces:
            pieces_positions.append(piece.position)
        return pieces_positions

    def get_all_valid_moves(self):
        """
        Get all valid moves of the player's pieces.

        :return: Returns all the valid moves of the player's pieces except the castling and en passant ones.
        I could not find a scenario where this function needs this information, but perhaps I am wrong.
        """
        moves_list = []
        for piece in self.pieces:
            piece_valid_moves = []
            if piece.type == "Pawn" or piece.type == "King":
                piece_valid_moves = piece.valid_moves[0]
            else:
                piece_valid_moves = piece.valid_moves
            moves_list.append(piece_valid_moves)
        return moves_list

    def get_pieces_by_type(self, type):
        """
        Get pieces by their type.

        :param type: The type of the pieces needed.
        :return: A list of all the pieces the player owns of the given type.
        """
        pieces_needed = []
        for piece in self.pieces:
            if piece.type == type:
                pieces_needed.append(piece)
        return pieces_needed

    def get_piece_by_position(self, position):
        """
        Get a piece by its position.

        :param position: Position in the form of a tuple.
        :return: Return the player's piece in that position. If there isn't one, return None.
        """
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def update_check(self, enemy_player):
        """
        Check if the king is in check by looking at all enemy valid moves.

        :param enemy_player: A player object of the rival player.
        :return: Doesn't return anything but updates the check parameter if the king is under attack.
        """
        king = self.get_pieces_by_type("King")[0]
        check = False
        if self.check:
            print("King is in check!")
        if not check:
            for piece_valid_moves in enemy_player.get_all_valid_moves():
                for move in piece_valid_moves:
                    if king.position == move:
                        check = True
                        break
                if check:
                    break
        self.check = check

    def check_check(self, enemy_player, current_pos, new_pos):
        """
        Check if a move puts the player's king in check.

        :param enemy_player: The enemy player.
        :param current_pos: Current position of the piece.
        :param new_pos: New position of the piece.
        :return: True if the move puts the king in check, False otherwise.
        """
        selected_piece = self.get_piece_by_position(current_pos)
        if self.get_pieces_by_type("King"):
            king_pos = self.get_pieces_by_type("King")[0].position
        else:
            return False
        selected_piece.update_position(new_pos)
        my_player_positions = self.get_all_positions()
        enemy_player_positions = enemy_player.get_all_positions()
        captured_piece = None

        # Check for Rook and Bishop attacks
        dict_pieces = {"Rook": [(1, 0), (-1, 0), (0, 1), (0, -1)], "Bishop": [(1, 1), (1, -1), (-1, 1), (-1, -1)]}
        for piece, directions in dict_pieces.items():
            for direction in directions:
                for i in range(1, 8):
                    pos_checked = (king_pos[0] + direction[0] * i, king_pos[1] + direction[1] * i)
                    if pos_checked in my_player_positions or not InBoard(pos_checked):
                        break
                    elif pos_checked in enemy_player_positions:
                        attack_piece = enemy_player.get_piece_by_position(pos_checked)
                        if attack_piece.type == piece or attack_piece.type == "Queen":
                            selected_piece.update_position(current_pos)
                            if captured_piece:
                                enemy_player.add_piece(captured_piece)
                            return True

        # Check for Pawn attacks
        if self.color == 'white':
            offset = 1
        else:
            offset = -1
        attack_pawn_positions = [(king_pos[0] + 1, king_pos[1] + offset), (king_pos[0] - 1, king_pos[1] + offset)]
        enemy_pawns = enemy_player.get_pieces_by_type("Pawn")
        if enemy_pawns:
            for pawn in enemy_pawns:
                if pawn.position in attack_pawn_positions:
                    selected_piece.update_position(current_pos)
                    if captured_piece:
                        enemy_player.add_piece(captured_piece)
                    return True

        # Check for Knight attacks
        attack_knight_positions = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        enemy_knights = enemy_player.get_pieces_by_type("Knight")
        if enemy_knights:
            for knight in enemy_knights:
                for pos in attack_knight_positions:
                    pos_checked = (king_pos[0] + pos[0], king_pos[1] + pos[1])
                    if pos_checked == knight.position:
                        if captured_piece:
                            enemy_player.add_piece(captured_piece)
                        selected_piece.update_position(current_pos)
                        return True

        if captured_piece:
            enemy_player.add_piece(captured_piece)
        selected_piece.update_position(current_pos)
        return False

    def update_pawns_valid_moves(self, enemy_player):
        """
        Update the valid moves of all the pawns.

        :param enemy_player: The enemy player.
        :return: None
        """
        pawns = self.get_pieces_by_type("Pawn")
        for pawn in pawns:
            pawn.update_valid_moves(self, enemy_player)

    def check_mate(self, enemy_player):
        """
        Check if the player is in checkmate.

        :param enemy_player: A player object of the rival player.
        :return: True if the player is in checkmate, False if they aren't.
        """
        if not self.check:
            return False

        king = self.get_pieces_by_type("King")[0]
        king.update_valid_moves(self, enemy_player)
        if king.valid_moves[0]:
            return False
        for piece in self.pieces:
            if piece.valid_moves:
                if piece.type == "Pawn" or piece.type == "King":
                    if piece.type == "King":
                        for piece_valid_move in piece.valid_moves[0]:
                            if not self.check_check(enemy_player, piece.position, piece_valid_move):
                                return False
                    else:
                        for piece_valid_move in piece.valid_moves[0]:
                            if not self.check_check(enemy_player, piece.position, piece_valid_move):
                                return False
                else:
                    for piece_valid_move in piece.valid_moves:
                        if not self.check_check(enemy_player, piece.position, piece_valid_move):
                            return False
        my_pawns = self.get_pieces_by_type("Pawn")  # check for attacking moves of the pawns
        if self.color == 'white':
            offset = 1
        else:
            offset = -1
        for pawn in my_pawns:
            pawns_attacking_moves = [(pawn.position[0] + 1, pawn.position[1] + offset), (pawn.position[0] - 1, pawn.position[1] + offset)]
            for move in pawns_attacking_moves:
                attack_piece = enemy_player.get_piece_by_position(move)
                if attack_piece is not None and not self.check_check(enemy_player, pawn.position, move):
                    return False
        print(f"No escape moves found. Checkmate! The {self.color} player is checkmated")
        return True

    def check_stale_mate(self):
        """
        Check if the player is in stalemate.

        :return: True if the player is in stalemate, False otherwise.
        """
        if self.check:
            return False
        all_valid_moves = self.get_all_valid_moves()
        if not any(all_valid_moves):
            return True
        return False

    def draw_pieces(self, screen):
        """
        Draw all the pieces on the screen.

        :param screen: The game screen.
        :return: None
        """
        for piece in self.pieces:
            if piece:
                piece.draw(screen)

    def draw_captured_pieces(self, screen):
        """
        Draw all captured pieces on the screen.

        :param screen: The game screen.
        :return: None
        """
        if self.color == 'white':
            offset = 800  # Adjusted offset
        else:
            offset = 900  # Adjusted offset
        for i in range(len(self.capture_pieces)):
            captured_piece = self.capture_pieces[i]
            image = captured_piece.capture_drawing()  # Adjusted captured piece size
            screen.blit(image, (offset, 5 + 40 * i))  # Adjusted position

    def add_piece(self, piece):
        """
        Add a piece to the player's collection.

        :param piece: The piece to add.
        :return: None
        """
        self.pieces.append(piece)

    def add_captured_piece(self, piece):
        """
        Add a captured piece to the player's collection.

        :param piece: The captured piece to add.
        :return: None
        """
        self.capture_pieces.append(piece)

    def remove_piece(self, piece):
        """
        Remove a piece from the player's collection.

        :param piece: The piece to remove.
        :return: None
        """
        if piece in self.pieces:
            self.pieces.remove(piece)

    def initialize_player(self):
        """
        Initialize the player with pieces at their starting positions.

        :return: None
        """
        # Paths to images
        if self.color == 'white':
            starting_positions_white = [
                (4, 0),  # King
                (3, 0),  # Queen
                (0, 0), (7, 0),  # Rooks
                (2, 0), (5, 0),  # Bishops
                (1, 0), (6, 0),  # Knights
                [(i, 1) for i in range(8)]  # Pawns
            ]
            self.pieces = [
                               King(starting_positions_white[0], 'white'),
                               Queen(starting_positions_white[1], 'white'),
                               Rook(starting_positions_white[2], 'white'),
                               Rook(starting_positions_white[3], 'white'),
                               Bishop(starting_positions_white[4], 'white'),
                               Bishop(starting_positions_white[5], 'white'),
                               Knight(starting_positions_white[6], 'white'),
                               Knight(starting_positions_white[7], 'white')
                           ] + [Pawn(pos, 'white') for pos in starting_positions_white[8]]
            self.capture_pieces = []
        else:
            starting_positions_black = [
                (4, 7),  # King
                (3, 7),  # Queen
                (0, 7), (7, 7),  # Rooks
                (2, 7), (5, 7),  # Bishops
                (1, 7), (6, 7),  # Knights
                [(i, 6) for i in range(8)]  # Pawns
            ]
            self.pieces = [
                               King(starting_positions_black[0], 'black'),
                               Queen(starting_positions_black[1], 'black'),
                               Rook(starting_positions_black[2], 'black'),
                               Rook(starting_positions_black[3], 'black'),
                               Bishop(starting_positions_black[4], 'black'),
                               Bishop(starting_positions_black[5], 'black'),
                               Knight(starting_positions_black[6], 'black'),
                               Knight(starting_positions_black[7], 'black')
                           ] + [Pawn(pos, 'black') for pos in starting_positions_black[8]]
            self.capture_pieces = []
