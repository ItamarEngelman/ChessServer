import pygame
from King import King
from Queen import Queen
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Pawn import Pawn

class Player():
    def __init__(self, color):
        self.color = color
        self.initialize_player()
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
                piece_valid_moves = piece_valid_moves
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
    def draw_pieces(self):
        for piece in self.pieces:
            piece.draw()
    def draw_captured_pieces(self,screen):
        if self.color == 'white':
            offset = 825
        else:
            offset = 925
        for i in range(len(self.capture_pieces)):
            captured_piece = self.capture_pieces[i]
            screen.blit(captured_piece.capture_drawing(), (offset, 5 + 50 * i))

    def initialize_player(self):
        # Paths to images
        if self.color=='white':
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




