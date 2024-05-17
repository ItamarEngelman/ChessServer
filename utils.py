def InBoard(position):
    if (position[0] > 7 or position[0] < 0) or (position[1] > 7 or position[1] < 0):
        return False
    return True


def eliminate_off_board(moves_list):
    correct_moves = []
    for move in moves_list:
        if InBoard(move):
            correct_moves.append(move)
    return correct_moves
def inside_lst(position, lst):
    for move in lst:
        if move == position:
            return True
    return False
def insdie_lst_of_lists(position, lst_of_lists):
    """

    :param position: a position thae we check if in the list of lists
    :param lst_of_lists: the list of lists that we check.
    :return: true if the position is in the lst_od_list and false if it isn't
    """
    for lst in lst_of_lists:
        for item in lst:
            if position == item:
                return True
    return False
def find_attacking_piece(position, enemy_player):
    """

    :param position: tuple - represent the position attacked
    :param enemy_player: a player object of the nemy player
    :return: the piece that attack the position. if there isn't - return None
    """
    for piece in enemy_player.pieces:
        if piece.valid_moves:
            if piece.type in ["Pawn", "King"]:
                for move in piece.valid_moves[0]:
                    if move == position:
                        return piece
            else:
                for move in piece.valid_moves:
                    if move == position:
                        return piece
    return None


def get_opposite_direction_by_value(dict_vectors, current_direction):
    """
    Finds the opposite direction in any vector category within dict_vectors.

    :param dict_vectors: Dictionary of direction categories and their vector tuples.
    :param current_direction: Tuple representing the current direction to find the opposite for.
    :return: The opposite direction if found, None if not found.
    """
    for directions in dict_vectors.values():
        if current_direction in directions:
            current_index = directions.index(current_direction)
            opposite_index = 1 - current_index  # This toggles between 0 and 1 for two-element lists
            return directions[opposite_index]
    return None
def get_key_by_value(d, value):
    """
    a function that searching for a key in a dict by value. return a  singe ( ! ) key.
    :param d: a dicinary where the key and the value is
    :param value: the value of key we are looking for
    :return: if the key is in  the dict, it return the key. if not, return None
    """
    for key, val in d.items():
        if val == value:
            return key
    return None
def create_move_msg(move_type, old_coords, new_coords):
    """Create a formatted message for a move."""
    old_coords_str = f"{old_coords[0]},{old_coords[1]}"
    new_coords_str = f"{new_coords[0]},{new_coords[1]}"
    return f"{move_type}?{old_coords_str}?{new_coords_str}"
def is_legal_move_format(move):
    try:
        move_type, from_pos, to_pos = move.split('?')
        from_pos = tuple(map(int, from_pos.split(',')))
        to_pos = tuple(map(int, to_pos.split(',')))
        return True
    except ValueError:
        return False
dict_of_promotions = {"Bishop": (8, 0), "Knight": (8, 1), "Rook": (8, 2), "Queen": (8, 3)}
print(get_key_by_value(dict_of_promotions, (8, 3)))
