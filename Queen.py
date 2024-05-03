from Piece import *
import pygame
class Queen(Piece):
    def __init__(self, image_path, position, color):
        self.image_path = image_path
        self.position = position
        self.color = color
        self.moved = False
        self.type = 'Queen'
        self.valid_moves = []
    def update_position(self, new_position):
        self.position = new_position
    def update_moved(self):
         self.moved = True
    def update_valid_moves(self, my_player, enemy_player):
        #print(f"in update_moves of queen")
        moves_list = []
        for i in range(4):  # down, up, right, left
            #print(" check rook moves for queen")
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
                pos_checked = (self.position[0] + (chain * x), self.position[1] + (chain * y))
                if pos_checked not in my_player.get_all_positions() and not my_player.check_check(enemy_player, self.position, pos_checked):
                    moves_list.append(pos_checked)
                    if pos_checked in enemy_player.get_all_positions():
                        path = False
                    if not InBoard(pos_checked):
                        path = False
                    chain += 1
                else:
                    path = False
        for i in range(4):  # up-right, up-left, down-right, down-left
            #print(" check bishop moves for queen")
            path = True
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            else:
                x = -1
                y = 1
            while path:
                pos_checked = (self.position[0] + (chain * x), self.position[1] + (chain * y))
                if pos_checked not in my_player.get_all_positions() and not my_player.check_check(enemy_player, self.position, pos_checked):
                    moves_list.append(pos_checked)
                    if pos_checked in enemy_player.get_all_positions():
                        path = False
                    if not InBoard(pos_checked):
                        path = False
                    chain += 1
                else:
                    path = False
        #print(f"valid_moves of queen - {moves_list}")
        moves_list = eliminate_off_board(moves_list)
        self.valid_moves = moves_list