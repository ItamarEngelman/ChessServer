from datetime import datetime

def create_log_file():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chess_game_{timestamp}.txt"
    with open(filename, 'a') as file:
        file.write(f"New game started!\nthe game started at {timestamp}\n")
    return filename

def log_move(filename, move, opponent_color):
    recorded_msg = ''
    if opponent_color == 'white':
        my_color = 'black'
    else:
        my_color = 'white'

    parts = move.split('?')
    if len(parts) == 3:
        move_type = parts[0]
        from_pos = parts[1]
        to_pos = parts[2]

        from_pos_tuple = tuple(map(int, from_pos.split(',')))
        to_pos_tuple = tuple(map(int, to_pos.split(',')))

        if move_type == 'quit':
            if opponent_color == 'white':
                recorded_msg = 'black has quit, white won'
            else:
                recorded_msg = 'white had quit, black won'
        elif move_type in ['white', 'black']:
            recorded_msg = f"{move_type} won the game"
        elif move_type == 'move':
            recorded_msg = f"{my_color} moved their piece from {from_pos_tuple} to {to_pos_tuple}"

    if recorded_msg:
        try:
            with open(filename, 'a') as file:
                file.write(recorded_msg + '\n')
        except Exception as e:
            print(e)


