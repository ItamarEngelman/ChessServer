import pygame
from King import King
from Queen import Queen
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Pawn import Pawn
from utils import *
class Player():
    def __init__(self, color, pieces, capture_pieces):
        self.color = color
        self.check = False
        self.pieces = pieces
        self.capture_pieces = capture_pieces
    def get_all_positions(self):
        pieces_positions = []
        for piece in self.pieces:
            pieces_positions.append(piece.position)
        return pieces_positions
    def get_all_valid_moves(self):
        """

        :return: the  functions return all the alid moves of the player's pieces except(!!!) the castling and en_passon ones.
        I could not find a scnerrio where this function needs this information, but pharps I am wrong.
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

        :param type: get the type  of the pieces needed
        :return: a list of all the pieces needed which the player own, according to the given type.
        """
        pieces_needed = []
        for piece in self.pieces:
            if piece.type == type:
                pieces_needed.append(piece)
        return pieces_needed
    def get_piece_by_position(self, position):
        """

        :param position: get a position in the form pf a tuple.
        :return: return the player piece in that position.  if there isn't one - return None
        """
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def update_check(self, enemy_player):
        """
        Check if the king is in check by looking at all enemy valid moves.

        :param enemy_player: a player object of the rival player
        :return: doesn't return anything but updates the check parameter if the king is being under attack.
        """
        king = self.get_pieces_by_type("King")[0]
        check = False  # Use the existing state directly if that's intended
        if self.check:
            print("king in in check !")
        if not check:  # Only process if we don't already know king is in check
            for piece_valid_moves in enemy_player.get_all_valid_moves():
                for move in piece_valid_moves:
                    if king.position == move:
                        check = True
                        break  # Breaks out of the inner loop only
                if check:
                    break  # Breaks out of the outer loop if king is in check
        self.check = check

    def check_check(self, enemy_player, current_pos, new_pos):
        selected_piece = self.get_piece_by_position(current_pos)
        king_pos = self.get_pieces_by_type("King")[0].position
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
        # my_pawns = self.get_pieces_by_type("Pawn")
        # for pawn in my_pawns:
        #     for pawn_valid_moves in pawn.valid_moves:
        #         if
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
        a function that update the valid moves of all the pawns.
        :param enemy_player:
        :return:
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
            if piece.valid_moves:  # Ensure valid_moves is not empty
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
            pawns_attacking_moves = [(pawn.position[0] + 1, pawn.position[1] + offset), (pawn.position[0] - 1,
                                                                                        pawn.position[1] + offset)]
            for move in pawns_attacking_moves:
                attack_piece = enemy_player.get_piece_by_position(move)
                if attack_piece is not None and not self.check_check(enemy_player, pawn.position, move):
                    return False
        print(f"No escape moves found. Checkmate! the {self.color} player is check_mated")
        return True


    def check_stale_mate(self):
        """
        a function that check if the player is in stale mate
        :return:
        """
        if self.check:
            return False
        all_valid_moves = self.get_all_valid_moves()
        if not any(all_valid_moves):
            return True
        return False

    def check_pawn_attacks(self, king, move, enemy_player):
        pass
        # original_pos = king.position
        # king.update_position(move)
        # pawns = enemy_player.get_pieces_by_type("Pawn")
        # if self.color == "white":
        #     offset = 2
        # else:
        #     offset = -2
        # pos_check = [(move[0] + 2, move[1] + offset), (move[0] - 2, move[1] + offset)]
        # pos_check = eliminate_off_board(pos_check)
        # for pawn, pos in zip(pawns, pos_check):
        #     if pawn.position == pos:
        #         pawn.update_valid_moves(self, enemy_player)
        # king.update_position(original_pos)

    def eliminate_all_pieces(self):
        for piece in self.pieces:
            if piece.type != "King":
                self.remove_piece(piece)

    def draw_pieces(self, screen):
        for piece in self.pieces:
            if piece:
                piece.draw(screen)

    def draw_captured_pieces(self, screen):
        if self.color == 'white':
            offset = 800  # Adjusted offset
        else:
            offset = 900  # Adjusted offset
        for i in range(len(self.capture_pieces)):
            captured_piece = self.capture_pieces[i]
            image = captured_piece.capture_drawing()  # Adjusted captured piece size
            screen.blit(image, (offset, 5 + 40 * i))  # Adjusted position

    def add_piece(self, piece):  # a function for testing the class and other functions
        self.pieces.append(piece)
    def add_captured_piece(self, piece):
        self.capture_pieces.append(piece)
    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)
    def initialize_player(self):
        # Paths to images
        if self.color == 'white':
            image_paths = {
                'King': 'assets/images/white king.png',
                'Queen': 'assets/images/white queen.png',
                'Rook': 'assets/images/white rook.png',
                'Bishop': 'assets/images/white bishop.png',
                'Knight': 'assets/images/white knight.png',
                'Pawn': 'assets/images/white pawn.png'
            }
            starting_positions_white = [
                (4, 0),  # King
                (3, 0),  # Queen
                (0, 0), (7, 0),  # Rooks
                (2, 0), (5, 0),  # Bishops
                (1, 0), (6, 0),  # Knights
                [(i, 1) for i in range(8)]  # Pawns
            ]
            self.pieces = [
                               King(image_paths['King'], starting_positions_white[0], 'white'),
                               Queen(image_paths['Queen'], starting_positions_white[1], 'white'),
                               Rook(image_paths['Rook'], starting_positions_white[2], 'white'),
                               Rook(image_paths['Rook'], starting_positions_white[3], 'white'),
                               Bishop(image_paths['Bishop'], starting_positions_white[4], 'white'),
                               Bishop(image_paths['Bishop'], starting_positions_white[5], 'white'),
                               Knight(image_paths['Knight'], starting_positions_white[6], 'white'),
                               Knight(image_paths['Knight'], starting_positions_white[7], 'white')
                           ] + [Pawn(image_paths['Pawn'], pos, 'white') for pos in starting_positions_white[8]]
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
            image_paths_black = {
                'King': 'assets/images/black king.png',
                'Queen': 'assets/images/black queen.png',
                'Rook': 'assets/images/black rook.png',
                'Bishop': 'assets/images/black bishop.png',
                'Knight': 'assets/images/black knight.png',
                'Pawn': 'assets/images/black pawn.png'
            }
        # Initialize black pieces
            self.pieces = [
                               King(image_paths_black['King'], starting_positions_black[0], 'black'),
                               Queen(image_paths_black['Queen'], starting_positions_black[1], 'black'),
                               Rook(image_paths_black['Rook'], starting_positions_black[2], 'black'),
                               Rook(image_paths_black['Rook'], starting_positions_black[3], 'black'),
                               Bishop(image_paths_black['Bishop'], starting_positions_black[4], 'black'),
                               Bishop(image_paths_black['Bishop'], starting_positions_black[5], 'black'),
                               Knight(image_paths_black['Knight'], starting_positions_black[6], 'black'),
                               Knight(image_paths_black['Knight'], starting_positions_black[7], 'black')
                           ] + [Pawn(image_paths_black['Pawn'], pos, 'black') for pos in starting_positions_black[8]]
            self.capture_pieces = []




    # def check_check_mate(self,enemy_player,  new_pos):
    #
    #     """
    #     a function that implemented if the king is in cheak. it cheack for a move if he  lead to cheackmate (the king is under_attack even after he moves
    #     and can be captured by the enemy next turn) if all themoves leads to cheack mate, the player lose (in checkmate).
    #     :param enemy_player: a player object of the  rival player
    #     :param new_pos: the new position that the king is move to.
    #     :return: true if the king is under attack when he moved to the new position or not.
    #     """
    #
    #     king = self.get_pieces_by_type("King")[0]
    #     current_pos = king.position
    #     king.update_position(new_pos)
    #     for piece in enemy_player.pieces:
    #         if king.position == piece.position:
    #             current_piece = piece
    #             enemy_player.remove_piece(piece)
    #             for tool in enemy_player.pieces:
    #                 tool.update_valid_moves()
    #             for tool in enemy_player.pieces:
    #                 for move in tool.get_all_valid_moves():
    #                     if king.position == move:
    #                         king.update_position(current_pos)
    #                         enemy_player.add_piece(current_piece)
    #                         return True
    #             king.update_position(current_pos)
    #             enemy_player.add_piece(current_piece)
    #             return False
    #
    #         else:
    #             for move in piece.get_all_valid_moves():
    #                 if king.position == move:
    #                     king.update_position(current_pos)
    #                     return True
    #     king.update_position(current_pos)
    #     return False