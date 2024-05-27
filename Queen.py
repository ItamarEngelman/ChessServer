from Piece import *

class Queen(Piece):
    def __init__(self, position, color):
        self.position = position
        self.color = color  # Set the color attribute first
        if self.color == 'white':
            self.image_path = 'assets/images/white queen.png'
        else:
            self.image_path = 'assets/images/black queen.png'
        self.moved = False
        self.type = 'Queen'
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
        for i in range(4):  # up-right, up-left, down-right, down-left
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
                position_checked = (self.position[0] + (chain * x), self.position[1] + (chain * y))
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

        moves_list = eliminate_off_board(moves_list)
        self.valid_moves = moves_list
