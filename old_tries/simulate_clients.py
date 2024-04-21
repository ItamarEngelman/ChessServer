import socket
import threading
import time

HOST = '127.0.0.1'  # Standard loopback interface (localhost)
PORT = 65432
def simulate_client(HOST, PORT, client_name, move):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to the server
        sock.connect((HOST, PORT))
        print(f"{client_name} connected to chess server.")

        # Send a move to the server
        print(f"{client_name} sending move: {move}")
        sock.sendall(move.encode('utf-8'))

        # Wait to receive a move from the server
        received_move = sock.recv(1024).decode('utf-8')
        print(f"{client_name} received move: {received_move}")


def main():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 65432

    # Simulate first client (Player 1)
    threading.Thread(target=simulate_client, args=(SERVER_HOST, SERVER_PORT, "Player 1", "e2e4")).start()

    # Wait a bit for the server to process (only necessary for the simulation)
    time.sleep(1)

    # Simulate second client (Player 2)
    threading.Thread(target=simulate_client, args=(SERVER_HOST, SERVER_PORT, "Player 2", "e7e5")).start()


if __name__ == "__main__":
    main()
