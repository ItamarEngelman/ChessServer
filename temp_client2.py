import time
import pygame
import socket
import threading
import queue
from Game import *
from utils import create_move_msg, is_legal_move_format

# Global flag to control the main loop
game_running = True

def setup_network():
    """
      Set up the client socket for network communication.

      :return: The client socket.
      """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    client_socket.setblocking(1)  # Temporarily set to blocking mode to receive initial color message
    return client_socket

def quit_socket(client_socket, is_pygame_initialized, which_side, game, my_color):
    """
       Quit the socket and optionally pygame based on which side is quitting.

       :param client_socket: The client socket to close.
       :param is_pygame_initialized: Flag indicating if pygame is initialized.
       :param which_side: The side to quit ('me' or 'opponent').
       :param game: The game object.
       :param my_color: The color of the client player.
       """
    if which_side == "me":
        client_socket.close()
        if is_pygame_initialized:
            pygame.quit()
    elif which_side == "opponent":
        if my_color == 'black':
            this_turn_player = game.white_player
            other_turn_player = game.black_player
        else:
            this_turn_player = game.black_player
            other_turn_player = game.white_player
        game.draw_other_player_quit(this_turn_player, other_turn_player)
        time.sleep(3)
        client_socket.close()
        if is_pygame_initialized:
            pygame.quit()

def listen_for_moves(client_socket, move_queue, is_pygame_initialized, game, my_color):
    """
    Listen for moves from the server and put them in the move queue.

    :param client_socket: The client socket to receive data from.
    :param move_queue: The queue to store received moves.
    :param is_pygame_initialized: Flag indicating if pygame is initialized.
    :param game: The game object.
    :param my_color: The color of the client player.
    """
    global game_running
    try:
        while game_running:
            try:
                data = client_socket.recv(1024).decode()
                if data:
                    print(f"Received move from server: {data}")
                    move_queue.put(data)
            except BlockingIOError:
                continue
            except ConnectionResetError as e:
                if game_running:
                    quit_socket(client_socket, is_pygame_initialized, "opponent", game, my_color)
                    print(f"Connection reset error: {e}")
    except Exception as e:
        if game_running:
            print(f"Error receiving data: {e}")
            quit_socket(client_socket, is_pygame_initialized, "opponent", game, my_color)

def process_move_queue(move_queue, game, my_color, client_socket, is_pygame_initialized):
    """
       Process the move queue by handling each received move.

       :param move_queue: The queue containing moves.
       :param game: The game object.
       :param my_color: The color of the client player.
       :param client_socket: The client socket for communication.
       :param is_pygame_initialized: Flag indicating if pygame is initialized.
       """
    global game_running
    if not move_queue.empty():
        print(f"Move queue: {move_queue}")
        move = move_queue.get()
        if move:
            try:
                print(f"Processing move from queue: {move}")
                handle_received_moves(move, game, my_color, move_queue, client_socket, is_pygame_initialized)
            except Exception as e:
                print(f"Error processing received move: {e}")

def handle_received_moves(move, game, my_color, move_queue, client_socket, is_pygame_initialized):
    """
       Handle the received move based on its type.

       :param move: The received move.
       :param game: The game object.
       :param my_color: The color of the client player.
       :param move_queue: The queue containing moves.
       :param client_socket: The client socket for communication.
       :param is_pygame_initialized: Flag indicating if pygame is initialized.
       """
    global game_running
    if my_color == 'black':
        this_turn_player = game.white_player
        other_turn_player = game.black_player
    else:
        this_turn_player = game.black_player
        other_turn_player = game.white_player

    move_type, from_pos, to_pos = move.split('?')
    from_pos = tuple(map(int, from_pos.split(',')))
    to_pos = tuple(map(int, to_pos.split(',')))
    if move_type == 'quit':
        quit_socket(client_socket, is_pygame_initialized, 'opponent', game, my_color)
        game_running = False  # Stop the game
    elif move_type == 'winner':
        game.draw_game_over()  # Display game over screen
        time.sleep(3)
        game.winner = True  # Mark the game as having a winner
        quit_socket(client_socket, is_pygame_initialized, 'me', game, my_color)
        # if is_pygame_initialized:
        #     pygame.quit()
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

def main():
    global game_running
    pygame.init()
    is_pygame_initialized = True

    client_socket = setup_network()

    try:
        my_color = client_socket.recv(1024).decode()
        print(f"Assigned color: {my_color}")
    except Exception as e:
        print(f"Error receiving color assignment: {e}")
        client_socket.close()
        pygame.quit()
        return

    client_socket.setblocking(0)  # Set back to non-blocking mode after receiving color

    white_player = Player('white', [], [])
    black_player = Player('black', [], [])
    white_player.initialize_player()
    black_player.initialize_player()
    game = Game(white_player, black_player, my_color)

    move_queue = queue.Queue()
    threading.Thread(target=listen_for_moves, args=(client_socket, move_queue, is_pygame_initialized, game, my_color), daemon=True).start()

    while game_running:
        game.run_game()
        if my_color == 'white':
            this_turn_player = game.white_player
            other_turn_player = game.black_player
        else:
            this_turn_player = game.black_player
            other_turn_player = game.white_player
        if game.should_quit:
            move_msg = create_move_msg('quit', (-1, -1), (-1, -1))
            try:
                client_socket.sendall(move_msg.encode())
                quit_socket(client_socket, is_pygame_initialized, "me", game, my_color)
            except Exception as e:
                print(f"Error sending quit message: {e}")
            game_running = False
            is_pygame_initialized = False
            break
        if game.move_type is not None and game.my_color == game.this_turn_color:
            move_msg = create_move_msg(game.move_type, game.chosen_piece_pos, game.last_move_to)
            print(f"move message is : {move_msg}")
            if is_legal_move_format(move_msg):
                try:
                    print(f"Sending move to server: {move_msg}")
                    client_socket.sendall(move_msg.encode())
                    if game.move_taken:
                        game.reset_turn(this_turn_player, other_turn_player)
                except Exception as e:
                    print(f"Error sending move: {e}")
        process_move_queue(move_queue, game, my_color, client_socket, is_pygame_initialized)
        if white_player.check_mate(black_player) or black_player.check_mate(white_player):
            client_socket.sendall(create_move_msg('winner', game.chosen_piece_pos, game.last_move_to).encode())
            game.draw_game_over()  # Display game over screen
            time.sleep(3)
            quit_socket(client_socket, is_pygame_initialized, 'me', game, my_color)

        if is_pygame_initialized:
            pygame.display.flip()

    client_socket.close()
    pygame.quit()

if __name__ == "__main__":
    main()

