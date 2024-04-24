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
        print(f"in update_moves of queen")
        moves_list = []
        for i in range(4):  # down, up, right, left
            print(" check rook moves for queen")
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
                if (
                self.position[0] + (chain * x), self.position[1] + (chain * y)) not in my_player.get_all_positions():
                    moves_list.append((self.position[0] + (chain * x), self.position[1] + (chain * y)))
                    if (self.position[0] + (chain * x), self.position[1] + (chain * y)) in enemy_player.get_all_positions():
                        path = False
                    chain += 1
                else:
                    path = False
        for i in range(4):  # up-right, up-left, down-right, down-left
            print(" check bishop moves for queen")
            new_path = True
            new_chain = 1
            if i == 0:
                a = 1
                b = -1
            elif i == 1:
                a = -1
                b = -1
            elif i == 2:
                a = 1
                b = 1
            else:
                a = -1
                b = 1
            while new_path:
                if (self.position[0] + (new_chain * a), self.position[1] + (new_chain * b)) not in my_player.get_all_positions():
                    moves_list.append((self.position[0] + (new_chain * a), self.position[1] + (new_chain * b)))
                    if (self.position[0] + (new_chain * a), self.position[1] + (new_chain * b)) in enemy_player.get_all_positions():
                        new_path = False
                    new_chain += 1
                else:
                    new_path = False
        print(f"valid_moves of queen - {moves_list}")
        moves_list = eliminate_off_board(moves_list)
        self.valid_moves = moves_list