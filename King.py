from Piece import *
import pygame
import math
class King(Piece):
    def __init__(self, image_path, position, color):
        self.image_path = image_path
        self.position = position
        self.color = color
        self.moved = False
        self.type = 'King'
        self.valid_moves = ([], [])
    def update_position(self, new_position):
        self.position = new_position
    def update_moved(self):
        self.moved = True
    def update_valid_moves(self, my_player, enemy_player):#  מחזיר מהלכי המלך רגילים ומהלכי "הצרחה". ההצרחה בודקת רק אם המלך זז  (כי אין לנו מידע נוסף בתוך מחלקה)
        regular_moves = []
        castling_moves = self.check_castling(my_player, enemy_player)
        # 8 squares to check for kings, they can go one square any direction
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for i in range(8):
            target = (self.position[0] + targets[i][0], self.position[1] + targets[i][1])
            regular_moves.append(target)
        regular_moves = eliminate_off_board(regular_moves)
        self.valid_moves = (regular_moves, castling_moves) # איבר ראשון שמחזיר הוא המהלכים הרגילים, האיבר שני זה מהלכי הצרחה פוטנציאלים.
    def check_castling(self, my_player, enemy_player):
        """

        :param my_player: player object which represent the player who owns the king and playing the current turn
        :param enemy_player:  player object which represent the other player
        :return: all the possible castling moves
        """
        castle_moves = []
        if self.color == 'white':
            off_set = 0
        else:
            off_set = 7
        if self.moved == True:
            return castle_moves
        rooks_lst = my_player.get_pieces_by_type("Rook") # a function the supposed to return a list  with all the rooks objects of the player.
        for rook in rooks_lst:
            if rook.moved == True:
                rooks_lst.remove(rook)
        for rook in rooks_lst:
            clean_path = True
            distance = abs(self.position[0] - rook.position[0])
            for i in range(distance):
                if rook.position[0] > self.position[0]:
                    if (insdie_lst_of_lists((self.position[0] + i, self.position[1]), enemy_player.get_all_valid_moves())) or \
                     (insdie_lst_of_lists((self.position[0] + i, self.position[1]), my_player.get_all_positions())):
                        clean_path = False
                if rook.position[0] < self.position[0]:
                    if (insdie_lst_of_lists((rook.position[0] + i, rook.position[1]), enemy_player.get_all_valid_moves())) or \
                     (insdie_lst_of_lists((rook.position[0] + i, rook.position[1]), my_player.get_all_positions())):
                        clean_path = False
            if clean_path == True:
                if rook.position[0] == 0:
                    castle_moves.append([(1, off_set), (2, off_set)])
                if rook.position[0] == 7:
                    castle_moves.append([(5, off_set), (4, off_set)])
        return castle_moves







