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
dict_of_promotions = {"Bishop": (8, 0), "Knight": (8, 1), "Rook": (8, 2), "Queen": (8, 3)}
print(get_key_by_value(dict_of_promotions, (8, 3)))
