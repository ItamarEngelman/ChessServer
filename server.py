import socket
import threading
import time
from utils import create_move_msg, is_socket_open
from aes_utilities import MyCipher
from server_games_record import create_log_file, log_move

def client_thread(conn, opponent_conn, my_color, cipher, log_filename):
    """
    A function that handles the communication between one client and another. Each thread represents one client,
    representing one player. It receives a move from its player (conn) and sends it to the opposing player in the right format.
    :param conn: the socket of the player/client that the thread represents.
    :param opponent_conn: the socket of the enemy player/client.
    :param my_color: the color of the client/player, assigned in the main loop of the server.
    :param cipher: the encryption cipher.
    :param log_filename: the filename of the log file.
    :return: None
    """
    try:
        if is_socket_open(conn):
            conn.sendall(my_color.encode())
        print(f"Sent color {my_color} to client")

        while True:
            encrypted_move = conn.recv(1024).decode()
            if not encrypted_move:
                print(f"No more data from {my_color} player, closing connection.")
                break

            nonce, ciphertext, tag = encrypted_move.split('|')
            move = cipher.aes_decryption(nonce, ciphertext, tag)

            print(f"Received move from {my_color}: {move}")
            log_move(log_filename, move, my_color)

            try:
                parts = move.split('?')
                if len(parts) == 3:
                    move_type = parts[0]
                    from_pos = parts[1]
                    to_pos = parts[2]

                    from_pos_tuple = tuple(map(int, from_pos.split(',')))
                    to_pos_tuple = tuple(map(int, to_pos.split(',')))

                    formatted_move = create_move_msg(move_type, from_pos_tuple, to_pos_tuple)

                    if is_socket_open(opponent_conn):
                        nonce, ciphertext, tag = cipher.aes_encryption(formatted_move)
                        encrypted_message = f"{nonce}|{ciphertext}|{tag}"
                        opponent_conn.sendall(encrypted_message.encode())

                    if move_type == "quit" or move_type in ['black', 'white']:
                        time.sleep(5)
                        print(f"No more data from {my_color} player, closing connections.")
                        if is_socket_open(conn):
                            conn.close()
                        if is_socket_open(opponent_conn):
                            nonce, ciphertext, tag = cipher.aes_encryption(move)
                            encrypted_message = f"{nonce}|{ciphertext}|{tag}"
                            opponent_conn.sendall(encrypted_message.encode())
                            opponent_conn.close()
                        return
                else:
                    print(f"Invalid move format received from {my_color}")
            except Exception as e:
                print(f"Error processing move from {my_color}: {e}")

    except Exception as e:
        pass

    finally:
        if is_socket_open(conn):
            conn.close()
        if is_socket_open(opponent_conn):
            opponent_conn.close()

def main():
    host = '0.0.0.0'
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print("Server started. Waiting for connections...")

    active_games = []

    try:
        connections = []

        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            connections.append(conn)

            if len(connections) % 2 == 0:
                player1 = connections[-2]
                player2 = connections[-1]

                key = b'Sixteen byte key'
                cipher = MyCipher(key)

                log_filename = create_log_file()

                game_thread1 = threading.Thread(target=client_thread, args=(player1, player2, 'white', cipher, log_filename), daemon=True)
                game_thread2 = threading.Thread(target=client_thread, args=(player2, player1, 'black', cipher, log_filename), daemon=True)
                game_thread1.start()
                game_thread2.start()
                active_games.append((game_thread1, game_thread2))

    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()
        print("Server socket closed.")
        for game_thread1, game_thread2 in active_games:
            game_thread1.join()
            game_thread2.join()

if __name__ == "__main__":
    main()





















# import socket
# import threading
# import time
# from utils import create_move_msg, is_legal_move_format, is_socket_open
# from aes_utils import MyCipher
# from server_games_record import log_move, create_log_file
# RESET_SIGNAL = "reset"
# WAITING_TIMEOUT = 5  # 5 seconds timeout for waiting players (adjust as needed)
#
# waiting_players = []  # List to keep track of players waiting for a new game
#
# games_files = []
# # Initialize MyCipher
# key = b'Sixteen byte key'  # Must be 16, 24, or 32 bytes long
# nonce = b'Unique nonce'    # Must be 16 bytes long
# cipher = MyCipher(key, nonce)
#
#
# def promote_waiting_players(waiting_players, connections):
#     current_time = time.time()
#     new_waiting_players = []
#     for player, start_time in waiting_players:
#         if current_time - start_time > WAITING_TIMEOUT:
#             print(f"Promoting waiting player to regular connection: {player}")
#             connections.append(player)
#         else:
#             new_waiting_players.append((player, start_time))
#     return new_waiting_players
#
# def client_thread(conn, opponent_conn, my_color):
#     global log_file
#
#     opponent_disconnected = False
#
#     try:
#         if is_socket_open(conn):
#             encrypted_msg, tag = cipher.aes_encryption(my_color)
#             conn.sendall(encrypted_msg + tag)
#         print(f"Sent color {my_color} to client")
#
#         while True:
#             try:
#                 encrypted_data = conn.recv(1024)
#                 if len(encrypted_data) < 16:
#                     print(f"Received invalid encrypted data from {my_color} player, closing connection.")
#                     break
#                 ciphertext, tag = encrypted_data[:-16], encrypted_data[-16:]  # Assuming the tag is 16 bytes long
#                 move = cipher.aes_decryption(ciphertext, tag)
#                 if not move:
#                     print(f"No more data from {my_color} player, closing connection.")
#                     break
#
#                 print(f"Received move from {my_color}: {move}")
#                 parts = move.split('?')
#                 if len(parts) == 3:
#                     move_type = parts[0]
#                     from_pos = parts[1]
#                     to_pos = parts[2]
#
#                     from_pos_tuple = tuple(map(int, from_pos.split(',')))
#                     to_pos_tuple = tuple(map(int, to_pos.split(',')))
#
#                     formatted_move = create_move_msg(move_type, from_pos_tuple, to_pos_tuple)
#                     if move_type == RESET_SIGNAL:
#                         print(f"{my_color} player requested a reset.")
#                         waiting_players.append((conn, time.time()))
#                         if len(waiting_players) >= 2:
#                             player1 = waiting_players.pop(0)
#                             player2 = waiting_players.pop(0)
#                             new_game_thread1 = threading.Thread(target=client_thread,
#                                                                 args=(player1[0], player2[0], 'white'), daemon=True)
#                             new_game_thread2 = threading.Thread(target=client_thread,
#                                                                 args=(player2[0], player1[0], 'black'), daemon=True)
#                             new_game_thread1.start()
#                             new_game_thread2.start()
#                         return
#                     if log_file:
#                         log_move(log_file, formatted_move, my_color)
#
#                     print(f"Forwarding move to opponent: {formatted_move}")
#                     if is_socket_open(opponent_conn) and not opponent_disconnected and move_type != RESET_SIGNAL:
#                         encrypted_msg, tag = cipher.aes_encryption(formatted_move)
#                         print(f"Sending encrypted move to opponent: {encrypted_msg + tag}")
#                         opponent_conn.sendall(encrypted_msg + tag)
#
#                     if move_type == "quit" or move_type in ['black', 'white']:
#                         print(f"{my_color} player has quit. Notifying opponent.")
#                         if is_socket_open(opponent_conn):
#                             encrypted_msg, tag = cipher.aes_encryption(move)
#                             opponent_conn.sendall(encrypted_msg + tag)
#                         if is_socket_open(conn) and move_type == "quit":
#                             conn.close()
#                             print(f"conn socket is closed.")
#                         time.sleep(10)
#                         opponent_disconnected = True
#                         break
#                 else:
#                     print(f"Invalid move format received from {my_color}")
#             except socket.error as e:
#                 if e.errno == 10053:
#                     print(f"Socket error for {my_color} player: {e}. Attempting to continue listening.")
#                 else:
#                     print(f"Socket error for {my_color} player: {e}")
#                     break
#     except Exception as e:
#         print(f"An error occurred in client_thread for {my_color}: {e}")
#
#     finally:
#         if is_socket_open(conn):
#             conn.close()
#         print(f"{my_color} player's connection closed.")
#         if is_socket_open(opponent_conn):
#             try:
#                 encrypted_msg, tag = cipher.aes_encryption("quit")
#                 opponent_conn.sendall(encrypted_msg + tag)
#             except Exception as e:
#                 print(f"Error notifying opponent: {e}")
#             opponent_conn.close()
# def main():
#     global log_file
#
#     host = '0.0.0.0'
#     port = 1709
#
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     server_socket.listen(10)
#     print("Server started. Waiting for connections...")
#
#     active_games = []
#     waiting_players = []
#
#     try:
#         connections = []
#
#         while True:
#             waiting_players = promote_waiting_players(waiting_players, connections)
#
#             conn, addr = server_socket.accept()
#             print(f"Connected by {addr}")
#             connections.append(conn)
#
#             if len(connections) % 2 == 0:
#                 player1 = connections[-2]
#                 player2 = connections[-1]
#
#                 log_file = create_log_file()
#                 games_files.append(log_file)
#
#                 game_thread1 = threading.Thread(target=client_thread, args=(player1, player2, 'white'), daemon=True)
#                 game_thread2 = threading.Thread(target=client_thread, args=(player2, player1, 'black'), daemon=True)
#                 game_thread1.start()
#                 game_thread2.start()
#                 active_games.append((game_thread1, game_thread2))
#
#     except KeyboardInterrupt:
#         print("Server is shutting down.")
#     finally:
#         server_socket.close()
#         print("Server socket closed.")
#         for game_thread1, game_thread2 in active_games:
#             game_thread1.join()
#             game_thread2.join()
#
# if __name__ == "__main__":
#     main()
