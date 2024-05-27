from Piece import *
class Knight(Piece):
    def __init__(self, position, color):
        """A function to initialize a knight piece

        Args:
            image_path (string): local path t
            position (tuple): _description_
            color (string): _description_
        """
        if color == 'white':
            self.image_path = 'assets/images/white knight.png'
        else:
            self.image_path = 'assets/images/black knight.png'
        self.position = position
        self.color = color
        self.moved = False
        self.type = 'Knight'
        if self.color == 'white':
            offset = 1
        else:
            offset = -1
        self.valid_moves = [(self.position[0] + 1, self.position[1] + 2 * offset),
                            (self.position[0] - 1, self.position[1] + 2 * offset)]
        self.valid_moves = eliminate_off_board(self.valid_moves)
    def update_position(self, new_position):
        self.position = new_position
    def update_moved(self):
        self.moved = True
    def update_valid_moves(self, my_player, enemy_player):
        moves_list = []
        # 8 squares to check for knights, they can go two squares in one direction and one in another
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            target = (self.position[0] + targets[i][0], self.position[1] + targets[i][1])
            if target not in my_player.get_all_positions() and not my_player.check_check(enemy_player, self.position, target):
                moves_list.append(target)
        moves_list = eliminate_off_board(moves_list)
        self.valid_moves = moves_list

