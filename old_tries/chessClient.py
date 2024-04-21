import socket

def chess_client(server_host, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to the server
        sock.connect((server_host, server_port))
        print("Connected to chess server.")

        while True:
            # Input a move
            move = input("Enter your move (or type 'quit' to exit): ")
            if move.lower() == 'quit':
                break

            # Send the move to the server
            sock.sendall(move.encode('utf-8'))
            print(f"Move sent: {move}")

            # Wait for and print the opponent's move received from the server
            opponent_move = sock.recv(1024).decode('utf-8')
            print(f"Opponent's move: {opponent_move}")

if __name__ == "__main__":
    SERVER_HOST = '127.0.0.1'  # The server's hostname or IP address
    SERVER_PORT = 65432        # The port used by the server
    chess_client(SERVER_HOST, SERVER_PORT)
