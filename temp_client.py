import time
import pygame
import socket
import threading
import queue
from Game import *
from utils import create_move_msg, is_legal_move_format, is_socket_open

new_socket = None
new_game = None

def setup_network():
    """
    Set up the client socket for network communication.

    :return: The client socket.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 65432))
        client_socket.setblocking(1)  # Temporarily set to blocking mode to receive initial color message
        return client_socket
    except Exception as e:
        print(f"Error setting up network: {e}")
        return None

def handle_waiting_for_reset(game, timeout=30):
    """
    Handle the waiting for reset logic. This function waits for a new connection
    from the server when the opponent retires.

    :param game: The game object.
    :param timeout: Time in seconds to wait for a new connection.
    """
    global new_socket, new_game
    start_time = time.time()
    while time.time() - start_time < timeout:
        if game.my_color == 'white':
            this_turn_player, other_turn_player = game.white_player, game.black_player
        else:
            this_turn_player, other_turn_player = game.black_player, game.white_player
        game.draw_turn(this_turn_player)
        pygame.display.flip()
        time.sleep(1)  # Adjust as necessary to control loop speed
        # Attempt to reconnect to the server
        new_socket = setup_network()
        if new_socket:
            try:
                new_color = new_socket.recv(1024).decode()
                print(f"Assigned color: {new_color}")
                if new_color:
                    # Create a new game object
                    white_player = Player('white', [], [])
                    black_player = Player('black', [], [])
                    white_player.initialize_player()
                    black_player.initialize_player()
                    new_game = Game(white_player, black_player, new_color)
                    return
            except Exception as e:
                print(f"Error receiving color assignment: {e}")
                if new_socket:
                    new_socket.close()
        time.sleep(3)  # Delay between reconnection attempts

    new_socket = None
    new_game = None  # Timeout reached, reset globals to None

def quit_socket(client_socket, is_pygame_initialized, which_side=None):
    """
    Quit the socket and optionally pygame based on which side is quitting.

    :param client_socket: The client socket to close.
    :param is_pygame_initialized: Flag indicating if pygame is initialized.
    :param which_side: The side to quit ('me' or 'opponent'). Optional.
    """
    if client_socket:
        time.sleep(1)  # Delay to ensure message is processed
        try:
            client_socket.close()
        except socket.error as e:
            print(f"Error closing socket: {e}")

    if is_pygame_initialized and which_side != "opponent":
        pygame.quit()

def quit_game(client_socket, is_pygame_initialized, game, which_side=None):
    global new_socket, new_game
    """
    Handle quitting the game and checking for reset.

    :param client_socket: The client socket to close.
    :param is_pygame_initialized: Flag indicating if pygame is initialized.
    :param game: The game object.
    :param which_side: The side to quit ('me' or 'opponent'). Optional.
    """
    if which_side == "opponent":
        if game.my_color == 'white':
            this_turn_player, other_turn_player = game.white_player, game.black_player
        else:
            this_turn_player, other_turn_player = game.black_player, game.white_player
        game.winner = this_turn_player.color
        game.game_over = True
        game.draw_other_player_quit(this_turn_player, other_turn_player)
        time.sleep(2)
        game.draw_game_over()
        want_reset = game.check_reset()
        game.check_quit_temporary = True
        if want_reset:
            client_socket.sendall("reset")
            handle_waiting_for_reset(game)
        else:
            time.sleep(3)  # Delay to ensure the player sees the opponent's quit screen
    game.check_quit_temporary = True
    quit_socket(client_socket, is_pygame_initialized, which_side)

def listen_for_moves(client_socket, move_queue, is_pygame_initialized, game, game_running_ref):
    """
    Listen for moves from the server and put them in the move queue.

    :param client_socket: The client socket to receive data from.
    :param move_queue: The queue to store received moves.
    :param is_pygame_initialized: Flag indicating if pygame is initialized.
    :param game: The game object.
    :param game_running_ref: A reference to the game running state (list with one boolean element).
    """
    try:
        while game_running_ref[0] and is_socket_open(client_socket) and not game.should_quit and not game.check_quit_temporary:
            try:
                if not isinstance(client_socket, socket.socket):
                    print("Invalid socket detected.")
                    break
                data = client_socket.recv(1024).decode()
                if data:
                    print(f"Received move from server: {data}")
                    move_queue.put(data)
            except BlockingIOError:
                pass  # Just pass on BlockingIOError to try receiving again
            except ConnectionResetError as e:
                quit_socket(client_socket, is_pygame_initialized, "opponent")
                print(f"Connection reset error: {e}")
                game_running_ref[0] = False
                break  # Exit the loop if connection is reset
            except socket.error as e:
                print(f"Socket error: {e}")
                game_running_ref[0] = False
                break
    except Exception as e:
        print(f"Error receiving data: {e}")
        quit_socket(client_socket, is_pygame_initialized)
        game_running_ref[0] = False

def process_move_queue(move_queue, game, my_color, client_socket, is_pygame_initialized, game_running_ref):
    """
    Process the move queue by handling each received move.

    :param move_queue: The queue containing moves.
    :param game: The game object.
    :param my_color: The color of the client player.
    :param client_socket: The client socket for communication.
    :param is_pygame_initialized: Flag indicating if pygame is initialized.
    :param game_running_ref: A reference to the game running state (list with one boolean element).
    """
    if not move_queue.empty():
        print(f"Move queue: {move_queue}")
        move = move_queue.get()
        if move:
            try:
                print(f"Processing move from queue: {move}")
                handle_received_moves(move, game, my_color, client_socket, is_pygame_initialized, game_running_ref)
            except Exception as e:
                print(f"Error processing received move: {e}")
                print(f"The move is : {move}")

def handle_received_moves(move, game, my_color, client_socket, is_pygame_initialized, game_running_ref):
    """
    Handle the received move based on its type.

    :param move: The received move.
    :param game: The game object.
    :param my_color: The color of the client player.
    :param client_socket: The client socket for communication.
    :param is_pygame_initialized: Flag indicating if pygame is initialized.
    :param game_running_ref: A reference to the game running state (list with one boolean element).
    """
    if my_color == 'black':
        this_turn_player, other_turn_player = game.white_player, game.black_player
    else:
        this_turn_player, other_turn_player = game.black_player, game.white_player

    move_type, from_pos, to_pos = move.split('?')
    from_pos = tuple(map(int, from_pos.split(',')))
    to_pos = tuple(map(int, to_pos.split(',')))
    if move_type == 'white' or move_type == 'black':
        game.winner = move_type
        game.game_over = True
        game.draw_game_over()  # Display game over screen
        time.sleep(3)
        quit_socket(client_socket, is_pygame_initialized, "me")
        game_running_ref[0] = False
    elif move_type == 'quit':
        time.sleep(1)
        game.draw_turn(this_turn_player)  # This includes draw_waiting_for_opponent()
        quit_game(client_socket, is_pygame_initialized, game, "opponent")
        game_running_ref[0] = False
    elif move_type == 'move':
        game.chose_piece(from_pos, this_turn_player, other_turn_player)
        game.execute_move(to_pos, this_turn_player, other_turn_player)
        if game.this_turn_selected_piece is not None and game.move_taken:
            game.reset_turn(this_turn_player, other_turn_player)
    elif move_type == 'promotion':
        new_type = get_key_by_value(dict_of_promotions, to_pos)
        promoted_piece = game.this_turn_selected_piece.promotion(new_type)
        this_turn_player.add_piece(promoted_piece)
        this_turn_player.remove_piece(game.this_turn_selected_piece)
        game.move_taken = True
        game.reset_turn(this_turn_player, other_turn_player)

def main(new_socket=None, new_game=None):
    pygame.init()
    is_pygame_initialized = True
    game_running_ref = [True]

    if new_socket and new_game:
        client_socket = new_socket
        game = new_game
        my_color = game.my_color
    else:
        client_socket = setup_network()
        if not client_socket:
            return  # Exit if network setup failed
        try:
            my_color = client_socket.recv(1024).decode()
            print(f"Assigned color: {my_color}")
        except Exception as e:
            print(f"Error receiving color assignment: {e}")
            if client_socket:
                client_socket.close()
            if is_pygame_initialized:
                pygame.quit()
            return

        client_socket.setblocking(0)  # Set back to non-blocking mode after receiving color

        white_player = Player('white', [], [])
        black_player = Player('black', [], [])
        white_player.initialize_player()
        black_player.initialize_player()
        game = Game(white_player, black_player, my_color)

    move_queue = queue.Queue()
    threading.Thread(target=listen_for_moves,
                     args=(client_socket, move_queue, is_pygame_initialized, game, game_running_ref),
                     daemon=True).start()

    while game_running_ref[0] and is_socket_open(client_socket):
        color_won = None
        game.run_game()

        if my_color == 'white':
            this_turn_player, other_turn_player = game.white_player, game.black_player
        else:
            this_turn_player, other_turn_player = game.black_player, game.white_player
        if game.should_quit:
            move_msg = create_move_msg('quit', (-1, -1), (-1, -1))
            try:
                client_socket.sendall(move_msg.encode())
                game_running_ref[0] = False
                time.sleep(1)
                quit_socket(client_socket, is_pygame_initialized)
            except Exception as e:
                print(f"Error sending quit message: {e}")
            game_running_ref[0] = False
            break
        if this_turn_player.check:
            if this_turn_player.check_mate(other_turn_player):
                color_won = other_turn_player.color
        if other_turn_player.check:
            if other_turn_player.check_mate(this_turn_player):
                color_won = this_turn_player
        if game.move_type is not None and game.my_color == game.this_turn_color:
            move_msg = create_move_msg(game.move_type, game.chosen_piece_pos, game.last_move_to)
            color_won = game.move_type  # since reset_turn function reset move_type into None
            print(f"Move message is : {move_msg}")
            if is_legal_move_format(move_msg) and is_socket_open(client_socket):
                try:
                    print(f"Sending move to server: {move_msg}")
                    client_socket.sendall(move_msg.encode())
                    if game.move_taken:
                        game.reset_turn(this_turn_player, other_turn_player)
                except Exception as e:
                    print(f"Error sending move to server: {e}")
            if game.move_type == "quit":
                quit_socket(client_socket, is_pygame_initialized)

        if color_won == "white" or color_won == "black":
            game.winner = color_won
            game.game_over = True
            game.draw_game_over()  # Display game over screen
            move_msg = create_move_msg(color_won, game.chosen_piece_pos, game.last_move_to)
            client_socket.sendall(move_msg.encode())
            time.sleep(3)
            quit_socket(client_socket, is_pygame_initialized)
            game_running_ref[0] = False

        process_move_queue(move_queue, game, my_color, client_socket, is_pygame_initialized, game_running_ref)

    print("Main game loop ended.")
    if new_socket and new_game:
        main(new_socket, new_game)
    else:
        quit_socket(client_socket, is_pygame_initialized)

if __name__ == "__main__":
    main(new_socket, new_game)
