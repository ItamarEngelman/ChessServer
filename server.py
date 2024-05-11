import socket
import threading
from Game import *

def client_thread(conn, opponent_conn, game):
    try:
        while True:
            move = conn.recv(1024).decode()
            if not move:
                break
            print(f"Received move: {move}")
            opponent_conn.sendall(move.encode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def main():
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 65432  # Port to listen on (non-privileged ports are > 1023)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Server started. Waiting for connections...")

    connections = []
  
    # Accept two clients
    while len(connections) < 2:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        connections.append(conn)

    if len(connections) == 2:
        player1, player2 = connections
        white_player = Player('white', [], [])
        black_player = Player('black', [], [])
        white_player.initialize_player()
        black_player.initialize_player()
        game = Game(white_player, black_player)
        # Start two threads to handle communication
        thread1 = threading.Thread(target=client_thread, args=(player1, player2, game))
        thread2 = threading.Thread(target=client_thread, args=(player2, player1, game))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    server_socket.close()

if __name__ == "__main__":
    main()
