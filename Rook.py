from Piece import *
import pygame
class Rook(Piece):

    def __init__(self, image_path, position, color):
        self.image_path = image_path
        self.position = position
        self.color = color
        self.moved = False
        self.type = 'Rook'
        self.valid_moves = []
    def update_position(self, new_position):
        self.position = new_position
    def update_moved(self):
        self.moved = True
    def update_valid_moves(self, my_player, enemy_player):
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