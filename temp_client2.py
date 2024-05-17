import time
import pygame
import socket
import threading
import queue
from Game import *
from utils import create_move_msg, is_legal_move_format

def setup_network():
    """
    This function creates the socket that is used by the client. The function is called in the main function.
    :return: client_socket
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    client_socket.setblocking(1)  # Temporarily set to blocking mode to receive initial color message
    return client_socket

def listen_for_moves(client_socket, move_queue):
    """
    This function listens for moves and if found, puts them in a queue.
    :param client_socket: the socket object of our client (established in the setup_network() function)
    :param move_queue: the move queue that saves the moves we receive from our opponent, to be executed in the main function.
    :return: None
    """
    try:
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if data:
                    print(f"Received move from server: {data}")
                    move_queue.put(data)
            except BlockingIOError:
                continue
    except Exception as e:
        print(f"Error receiving data: {e}")

def handle_received_moves(move, game, my_color):
    """
    This function handles the received moves and is implemented in the main function.
    :param move: a move of the opponent, from the move queue (built in the listen_for_moves function)
    :param game: the game object created for our client
    :param my_color: the color of our client
    :return: None
    """
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
        game.draw_other_player_quit()
        time.sleep(3)
        pygame.quit()
    elif move_type == 'winner':
        pass  # To be added
    else:
        if move_type:
            game.chose_piece(from_pos, this_turn_player, other_turn_player)
            game.execute_move(to_pos, this_turn_player, other_turn_player)
            if game.this_turn_selected_piece is not None:
                game.reset_turn(this_turn_player, other_turn_player)

def main():
    """
    The main function of the client. Creates a socket for the client with setup_network(), creates a game object
    for the client using the assigned color from the server, and uses a thread to listen to incoming moves from the opponent.
    :return: None
    """
    pygame.init()
    client_socket = setup_network()

    # Receive initial color message from the server
    try:
        my_color = client_socket.recv(1024).decode()
        print(f"Assigned color: {my_color}")
    except Exception as e:
        print(f"Error receiving color assignment: {e}")
        client_socket.close()
        return

    client_socket.setblocking(0)  # Set back to non-blocking mode after receiving color

    move_queue = queue.Queue()
    threading.Thread(target=listen_for_moves, args=(client_socket, move_queue), daemon=True).start()

    white_player = Player('white', [], [])
    black_player = Player('black', [], [])
    white_player.initialize_player()
    black_player.initialize_player()
    game = Game(white_player, black_player, my_color)  # Use assigned color

    running = True
    while running:
        # print(f"the game turn color: {game.this_turn_color}")
        # print(f"the player color : {my_color}")
        # print(f"In pause : {game.pause}")
        # time.sleep(0.5)
        game.run_game()
        if my_color == 'white':
            this_turn_player = game.white_player
            other_turn_player = game.black_player
        else:
            this_turn_player = game.black_player
            other_turn_player = game.white_player
        if game.should_quit:
            move_msg = create_move_msg('quit', (-1, -1), (-1, -1))
            client_socket.sendall(move_msg)
            pygame.quit()
        if game.move_taken and game.my_color == game.this_turn_color:
            move_msg = create_move_msg(game.move_type, game.chosen_piece_pos, game.last_move_to)
            if is_legal_move_format(move_msg):
                try:
                    print(f"Sending move to server: {move_msg}")
                    client_socket.sendall(move_msg.encode())
                    game.reset_turn(this_turn_player, other_turn_player)
                except Exception as e:
                    print(f"Error sending move: {e}")

        if not move_queue.empty():
            print(f"Move queue: {move_queue}")
            move = move_queue.get()
            if move:
                try:
                    print(f"Processing move from queue: {move}")
                    handle_received_moves(move, game, my_color)
                except Exception as e:
                    print(f"Error processing received move: {e}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    client_socket.close()
    pygame.quit()

if __name__ == "__main__":
    main()
