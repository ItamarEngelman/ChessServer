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



















