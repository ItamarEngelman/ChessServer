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

lst_of_lists = [[1,2],[9,11],[-4,5],[2,7]]
item = 2
print(insdie_lst_of_lists(item, lst_of_lists ))