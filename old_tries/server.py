import socket
import threading


class Server:
    def __init__(self, server_id, port):
        self.server_id = server_id
        self.port = port
        self.client_handlers = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(10)  # Listen for up to 10 queued connections
        print(f"Server {self.server_id} started on port {self.port}")

    def start(self):
        threading.Thread(target=self.accept_connections).start()

    def stop(self):
        print(f"Server {self.server_id} stopping")
        self.server_socket.close()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection established with {client_address}")
            client_handler = ClientHandler(client_socket)
            self.add_client_handler(client_handler)
            threading.Thread(target=client_handler.run).start()
            if len(self.client_handlers) % 2 == 0:
                self.start_game_if_possible()

    def start_game_if_possible(self):
        if len(self.client_handlers) >= 2:
            player1, player2 = self.client_handlers[:2]
            game_session = self.create_game_session(player1, player2)
            self.remove_client_handler(player1)
            self.remove_client_handler(player2)
            threading.Thread(target=game_session.start_game).start()

    def create_game_session(self, player1, player2):
        game_session = ChessGameSession(player1, player2)
        print(f"New game session created between {player1} and {player2}")
        return game_session

    def add_client_handler(self, client_handler):
        self.client_handlers.append(client_handler)
        print(f"Client handler {client_handler} added to the server")

    def remove_client_handler(self, client_handler):
        self.client_handlers.remove(client_handler)
        print(f"Client handler {client_handler} removed from the server")


class ChessGameSession:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        # Initialize Pygame chess game here

    def start_game(self):
        # Start the Pygame chess game interface
        pass

    # Additional methods for managing the chess game


class ClientHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def run(self):
        # Implement client communication logic here
        pass

    # Additional methods for handling client communication


# Main code to create and start the server
if __name__ == "__main__":
    server = Server(server_id=1, port=9999)
    server.start()
