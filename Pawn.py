from abc import ABC, abstractmethod
import pygame
from Piece import *
from Queen import *
from Rook import *
from Bishop import *
from Knight import *
class Pawn(Piece):
    """
    פעולה המייצגת אוביקטים מסוג פון. יורשת , כמו שאר החתיכות, ממחלקת חתיכה. מקבל את מיקום התמונה, את מיקום החייל והאם הפון זז או לא. הסוג הופך אוטומטית לסוג של פון. כמו כן , מקבל את הצבע של הפון

    """
    def __init__(self, image_path, position, color):
        """A function to initialize a pawn piece

        Args:
            image_path (string): local path t
            position (tuple): _description_
            color (string): _description_
            moved (bool, optional): _description_. Defaults to False.
        """
        self.image_path = image_path
        self.position = position
        self.color = color
        self.moved = False
        self.since_moved = 0
        self.type = 'Pawn'
        if self.color == 'white':
            offset = 1
        else:
            offset = -1
        self.valid_moves = ([(self.position[0],  self.position[1] + offset), (self.position[0],  self.position[1] + 2 * offset)], [])
    def update_position(self,  new_position):
        self.position = new_position
        self.since_moved = 0
    def update_moved(self):
        self.moved = True
    def update_since_moved(self):
        self.since_moved += 1

    def update_valid_moves(self, my_player, enemy_player):
        """

        :param my_player: player object which represent the player who owns the pawn and playing the current turn
        :param enemy_player:  represnt the player object who is againts us
        :return: update the valis_moves chrcristic - the first (in the  tuple) represnt the regular moves while the seacned represent the en_passon one. both lists full of tupples
        """
        moves_list = []
        ep_moves_list = self.check_ep(enemy_player)
        if self.color == 'white':
            offset = 1
        else:
            offset = -1
        if (self.position[0], self.position[1] + offset) not in my_player.get_all_positions() and \
                (self.position[0], self.position[1] + 1) not in enemy_player.get_all_positions():
            moves_list.append((self.position[0], self.position[1] + 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (self.position[0], self.position[1] + 2 * offset ) not in my_player.get_all_positions() and \
            (self.position[0], self.position[1] + 2 * offset) not in enemy_player.get_all_positions()\
            and self.moved is False:
                moves_list.append((self.position[0], self.position[1] + 2 * offset))
        if (self.position[0] + 1, self.position[1] + offset) in enemy_player.get_all_positions():
            moves_list.append((self.position[0] + 1, self.position[1] + offset))
        if (self.position[0] - 1, self.position[1] + offset) in enemy_player.get_all_positions():
            moves_list.append((self.position[0] - 1, self.position[1] + offset))
        self.valid_moves = (moves_list, ep_moves_list)
        # add en passant move checker
    def check_ep(self, enemy_player):
        """

        :param my_player: player object which represent the player who owns the pawn and playing the current turn
        :param enemy_player: represnt the player object who is againts us
        :return: all the ep moves possible of this pawn
        """
        ep_moves_list = []
        if self.color == 'white':
            offset = 4
        else:
            offset = 3
        for piece in enemy_player.pieces:  # ask ariel i do i confirm that the piece is removed
            if piece.type == "Pawn" and piece.position[1] == offset and piece.since_moved == 0:
                ep_moves_list.append(piece)
        return ep_moves_list
    def check_promotion(self):
        """

        :return: true if the pawn is in the end of the board and  false if it isn't
        """
        if self.color == 'white':
            offset = 7
        else:
            offset = 0
        if self.position[1] == offset:
            return True
        return False
    def promotion(self, new_type):
        """

                :param new_type: get the name of the new type wanted
                :return: an object of the type chosen. the object obtain the same Characteristics except the image and the type. the valid_moves doesn't change
                it only changed after update_valid_moves. if the new_type is diffrent than known ones - print that error occur and return None
                """
        if new_type == "Queen":
            return Queen(image_path_white_queen, self.position, self.color)
        if new_type == "Rook":
            return Rook(image_path_white_rook, self.position, self.color)
        if new_type == "Bishop":
            return Bishop(image_path_white_bishop,  self.position, self.color)
        if new_type == "Knight":
            return Knight(image_path_white_knight,  self.position, self.color)
        print("error had occur - problomatic type for promotion ")
        return None