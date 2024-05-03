import pygame
from King import King
from Queen import Queen
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Pawn import Pawn

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
        print(f"Debug: Checking if the king at position {king.position} is in check.")

        # Iterate over all valid moves of all pieces from the enemy player.
        for piece_valid_moves in enemy_player.get_all_valid_moves():
            for move in piece_valid_moves:
                # Print the move being checked against the king's position
                print(f"Debug: Checking enemy move {move} against king's position {king.position}.")
                if king.position == move:
                    # If a match is found, set check to True and break out of the loop
                    self.check = True
                    print(f"Debug: King is in check from move {move}.")
                    break
            # Break outer loop if check is found
            if self.check:
                break
        # Final status of check
        print(f"Debug: King check status is {self.check}.")

    def check_check(self, enemy_player, current_pos, new_pos):
        """
        a function that check for a move of a piece if after the move is implemended the king is in check
        :param enemy_player: a player object which represent the enemy player
        :param current_pos: the current pos of the piece being checked. with that pos we can find  the piece and after our checkinh, we will update the
        position of the piece again to the  current_pos
        :param new_pos: the new position caused by the  move that we check
        :return:  true if the king is in check after the move anf False if he isn't.
        """
        selected_piece = self.get_piece_by_position(current_pos)
        king = self.get_pieces_by_type("King")[0]
        selected_piece.update_position(new_pos)

        for piece_valid_moves in enemy_player.get_all_valid_moves():
            for move in piece_valid_moves:
                if king.position == move:
                    selected_piece.update_position(current_pos)
                    return True
        selected_piece.update_position(current_pos)
        return False


    def check_check_mate(self,enemy_player,  new_pos):

        """
        a function that implemented if the king is in cheak. it cheack for a move if he  lead to cheackmate (the king is under_attack even after he moves
        and can be captured by the enemy next turn) if all themoves leads to cheack mate, the player lose (in checkmate).
        :param enemy_player: a player object of the  rival player
        :param new_pos: the new position that the king is move to.
        :return: true if the king is under attack when he moved to the new position or not.
        """

        king = self.get_pieces_by_type("King")[0]
        current_pos = king.position
        king.update_position(new_pos)
        for piece in enemy_player.pieces:
            if king.position == piece.position:
                current_piece = piece
                enemy_player.remove_piece(piece)
                for tool in enemy_player.pieces:
                    tool.update_valid_moves()
                for tool in enemy_player.pieces:
                    for move in tool.get_all_valid_moves():
                        if king.position == move:
                            king.update_position(current_pos)
                            enemy_player.add_piece(current_piece)
                            return True
                king.update_position(current_pos)
                enemy_player.add_piece(current_piece)
                return False

            else:
                for move in piece.get_all_valid_moves():
                    if king.position == move:
                        king.update_position(current_pos)
                        return True
        king.update_position(current_pos)
        return False

    def check_mate(self, enemy_player):
        """

        :param enemy_player: a player object of the rival player.
        :return: return true if the player is  in cheack_mate, and False if he isn't.
        """
        if not self.check:
            return False
        king = self.get_pieces_by_type("King")[0]
        king.update_valid_moves(self, enemy_player)
        for move in king.valid_moves[0]:
            if not self.check_check_mate(self, enemy_player, king.position, move):
                return False
        return True

    def draw_pieces(self,screen):
        for piece in self.pieces:
            piece.draw(screen)
    def draw_captured_pieces(self,screen):
        if self.color == 'white':
            offset = 825
        else:
            offset = 925
        for i in range(len(self.capture_pieces)):
            captured_piece = self.capture_pieces[i]
            screen.blit(captured_piece.capture_drawing(), (offset, 5 + 50 * i))
    def add_piece(self,piece): # a  functionfor testing the class and other functions
        self.pieces.append(piece)
    def add_captured_piece(self,piece):
        self.capture_pieces.append(piece)
    def remove_piece(self, piece):
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




