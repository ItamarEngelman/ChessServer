import socket
import threading
import time
from datetime import datetime
from utils import create_move_msg, is_legal_move_format, is_socket_open

RESET_SIGNAL = "reset"
WAITING_TIMEOUT = 5  # 5 seconds timeout for waiting players (adjust as needed)

waiting_players = []  # List to keep track of players waiting for a new game

def create_log_file():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chess_game_{timestamp}.txt"
    if filename:
        with open(filename, 'a') as file:
            file.write("new game started !" + '\n')
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

        # Debugging: print received parts
        print(f"Received move type: {move_type}")
        print(f"Received from_pos: {from_pos}")
        print(f"Received to_pos: {to_pos}")

        # Ensure the positions are correctly formatted
        from_pos_tuple = tuple(map(int, from_pos.split(',')))
        to_pos_tuple = tuple(map(int, to_pos.split(',')))

        if move_type == 'quit':
            if opponent_color == 'white':
                recorded_msg = 'black has quit, white won'
            else:
                recorded_msg = 'white has quit, black won'
        elif move_type in ['white', 'black']:
            recorded_msg = f"{move_type} won the game"
        elif move_type == 'move':
            recorded_msg = f"{my_color} moved their piece from {from_pos_tuple} to {to_pos_tuple}"

    # Write the recorded message to the file
    if recorded_msg:
        with open(filename, 'a') as file:
            file.write(recorded_msg + '\n')

    # Debugging: print recorded message
    print(recorded_msg)


def promote_waiting_players(waiting_players, connections):
    """
    Promotes waiting players to the regular connection list if they have been waiting for too long.
    """
    current_time = time.time()
    new_waiting_players = []
    for player, start_time in waiting_players:
        if current_time - start_time > WAITING_TIMEOUT:
            print(f"Promoting waiting player to regular connection: {player}")
            connections.append(player)
        else:
            new_waiting_players.append((player, start_time))
    return new_waiting_players

def client_thread(conn, opponent_conn, my_color):
    """
    A function that handles the communication between one client and another. Each thread represents one client,
    representing one player. It receives a move from its player (conn) and sends it to the opposing player in the right format.
    :param conn: the socket of the player/client that the thread represents.
    :param opponent_conn: the socket of the enemy player/client.
    :param my_color: the color of the client/player, assigned in the main loop of the server.
    :return: None
    """
    global log_file

    try:
        # Send initial color message to the client
        if is_socket_open(conn):
            conn.sendall(my_color.encode('utf-8'))
        print(f"Sent color {my_color} to client")

        while True:
            try:
                move = conn.recv(1024).decode('utf-8')
                if not move:
                    print(f"No more data from {my_color} player, closing connection.")
                    break

                print(f"Received move from {my_color}: {move}")

                if move == RESET_SIGNAL:
                    print(f"{my_color} player requested a reset.")
                    # Add the player to the waiting list
                    waiting_players.append((conn, time.time()))
                    # Check if there are enough players to start a new game
                    if len(waiting_players) >= 2:
                        player1 = waiting_players.pop(0)
                        player2 = waiting_players.pop(0)
                        new_game_thread1 = threading.Thread(target=client_thread, args=(player1[0], player2[0], 'white'), daemon=True)
                        new_game_thread2 = threading.Thread(target=client_thread, args=(player2[0], player1[0], 'black'), daemon=True)
                        new_game_thread1.start()
                        new_game_thread2.start()
                    return

                try:
                    parts = move.split('?')
                    if len(parts) == 3:
                        move_type = parts[0]
                        from_pos = parts[1]
                        to_pos = parts[2]

                        # Debugging: print received parts
                        print(f"Received move type: {move_type}")
                        print(f"Received from_pos: {from_pos}")
                        print(f"Received to_pos: {to_pos}")

                        # Ensure the positions are correctly formatted
                        from_pos_tuple = tuple(map(int, from_pos.split(',')))
                        to_pos_tuple = tuple(map(int, to_pos.split(',')))

                        # Debugging: print converted tuples
                        print(f"Converted from_pos_tuple: {from_pos_tuple}")
                        print(f"Converted to_pos_tuple: {to_pos_tuple}")

                        formatted_move = create_move_msg(move_type, from_pos_tuple, to_pos_tuple)

                        # Log the move to the file
                        if log_file:
                            log_move(log_file, formatted_move, my_color)

                        # Debugging: print formatted move
                        print(f"Forwarding move to opponent: {formatted_move}")
                        if move_type == "quit" or move_type in ['black', 'white']:
                            print(f"{my_color} player has quit. Notifying opponent.")
                            if is_socket_open(opponent_conn):
                                opponent_conn.sendall(move.encode('utf-8'))
                            if is_socket_open(conn) and move_type == "quit":
                                conn.close()
                                print(f"conn socket is closed.")
                            time.sleep(10)
                            break
                        if is_socket_open(opponent_conn):
                            opponent_conn.sendall(formatted_move.encode('utf-8'))
                    else:
                        print(f"Invalid move format received from {my_color}")
                except Exception as e:
                    print(f"Error processing move from {my_color}: {e}")

            except socket.error as e:
                print(f"Socket error for {my_color} player: {e}")
                break

    except Exception as e:
        print(f"An error occurred in client_thread for {my_color}: {e}")

    finally:
        if is_socket_open(conn):
            conn.close()
        print(f"{my_color} player's connection closed.")
        if is_socket_open(opponent_conn):
            try:
                opponent_conn.sendall("quit".encode('utf-8'))  # Notify opponent about the disconnection
            except Exception as e:
                print(f"Error notifying opponent: {e}")
            opponent_conn.close()

def main():
    """
    The main function of the server. Creates a socket and when the number of connections is even, starts a new game.
    Each player gets their own thread and so each client thread has its own color.
    :return: None
    """
    global log_file

    host = '0.0.0.0'
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print("Server started. Waiting for connections...")

    active_games = []  # List to keep track of active game threads
    waiting_players = []  # List to keep track of players waiting for opponents

    try:
        connections = []

        while True:
            waiting_players = promote_waiting_players(waiting_players, connections)  # Promote waiting players if necessary

            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            connections.append(conn)

            if len(connections) % 2 == 0:
                # Start a new game with the last two connections
                player1 = connections[-2]
                player2 = connections[-1]

                # Create log file with the current timestamp
                log_file = create_log_file()

                game_thread1 = threading.Thread(target=client_thread, args=(player1, player2, 'white'), daemon=True)
                game_thread2 = threading.Thread(target=client_thread, args=(player2, player1, 'black'), daemon=True)
                game_thread1.start()
                game_thread2.start()
                active_games.append((game_thread1, game_thread2))  # Track the game threads

    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()
        if log_file:
            log_file.close()
        print("Server socket closed.")
        # Wait for all active game threads to finish
        for game_thread1, game_thread2 in active_games:
            game_thread1.join()
            game_thread2.join()

if __name__ == "__main__":
    main()
