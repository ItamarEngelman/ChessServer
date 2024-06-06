from pieces.Piece import *

class King(Piece):
    def __init__(self, position, color):
        if color == 'white':
            image_path = 'assets/images/white king.png'
        else:
            image_path = 'assets/images/black king.png'
        super().__init__(color, position, image_path)
        self.type = 'King'
        self.valid_moves = ([], [])
    def update_valid_moves(self, my_player, enemy_player):
        """
        Update the valid moves parameter of the king object.

        :param my_player: Player object of my current player
        :param enemy_player: Player object of the enemy player
        """
        regular_moves = []
        castle_moves = self.check_castling(my_player, enemy_player)
        print("Castle moves:", castle_moves)

        dict_vectors = {
            "Up-Down": [(0, 1), (0, -1)],
            "Left-Right": [(1, 0), (-1, 0)],
            "Diagonal-right": [(-1, 1), (1, -1)],
            "Diagonal-left": [(-1, -1), (1, 1)]
        }

        # Iterate over all vectors and directions to determine valid moves
        for vector, directions in dict_vectors.items():
            for direction in directions:
                pos_checked = (self.position[0] + direction[0], self.position[1] + direction[1])
                if pos_checked not in my_player.get_all_positions() and not insdie_lst_of_lists(pos_checked,
                                                                                                enemy_player.get_all_valid_moves()):
                    regular_moves.append(pos_checked)
                    # Immediately check if this move results in a capture of an attacking piece
                    attacking_piece = find_attacking_piece(pos_checked, enemy_player)
                    if attacking_piece and attacking_piece.type in ["Queen", "Bishop", "Rook"]:
                        # If capturing, assess the impact on the opposite direction
                        opposite = get_opposite_direction_by_value(dict_vectors, direction)
                        if opposite:
                            pos_opposite = (self.position[0] + opposite[0], self.position[1] + opposite[1])
                            if pos_opposite in regular_moves:
                                regular_moves.remove(pos_opposite)
                else:
                    attacking_piece = find_attacking_piece(pos_checked, enemy_player)
                    if attacking_piece:
                        if attacking_piece.type in ["Queen", "Bishop", "Rook"]:
                            opposite = get_opposite_direction_by_value(dict_vectors, direction)
                            if opposite and opposite in regular_moves:
                                regular_moves.remove(opposite)
                                print(f"Removed {opposite} due to {attacking_piece.type} threat at {pos_checked}")
                            break  # Exit the direction loop upon finding a threat

        regular_moves = eliminate_off_board(regular_moves)
        for move in regular_moves:
            if self.eliminate_moves_to_pawn_attacks(move, enemy_player):
                regular_moves.remove(move)
        self.valid_moves = (regular_moves, castle_moves)

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

        if self.moved or self.position in enemy_player.get_all_valid_moves():
            return castle_moves
        if my_player.check:
            return castle_moves

        rooks_lst = [rook for rook in my_player.get_pieces_by_type("Rook") if not rook.moved]

        for rook in rooks_lst:
            if self.position[1] != rook.position[1]:  # Ensure rook is in the same row as king
                continue
            clean_path = True
            start = min(self.position[0], rook.position[0]) + 1
            end = max(self.position[0], rook.position[0])
            for pos in range(start, end):
                pos_checked = (pos, self.position[1])
                if (pos_checked in my_player.get_all_positions() or  # check if the position is already occupied by a piece
                        pos_checked in enemy_player.get_all_positions()):
                    clean_path = False
                    break
                for piece in enemy_player.pieces:  # check if the position is attacked by an enemy piece
                    if piece.type != ('Pawn' or 'King') and pos_checked in piece.valid_moves:
                        clean_path = False
                        break
                    if piece.type == ('Pawn' or 'King') and pos_checked in piece.valid_moves[0]:
                        clean_path = False
                        break
            if clean_path:
                if rook.position[0] == 0:
                    castle_moves.append(((1, off_set), (2, off_set)))
                if rook.position[0] == 7:
                    castle_moves.append(((6, off_set), (5, off_set)))

        return castle_moves
    def eliminate_moves_to_pawn_attacks(self, move, enemy_player):
        original_pos = self.position
        self.update_position(move)

        pawns = enemy_player.get_pieces_by_type("Pawn")
        if self.color == "white":
            offset = 2
        else:
            offset = -2
        pos_check = [(move[0] + 2, move[1] + offset), (move[0] - 2, move[1] + offset)]
        pos_check = eliminate_off_board(pos_check)
        for pawn, pos in zip(pawns, pos_check):
            if pawn.position == pos:
                self.update_position(original_pos)
                return True
        self.update_position(original_pos)
        return False
