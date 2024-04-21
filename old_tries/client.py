import socket


def main():
    server_address = 'localhost'
    server_port = 9999

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_address, server_port))
        print("Connected to the server.")

        # Send a test message
        message = "Hello, server!"
        client_socket.sendall(message.encode())
        print(f"Sent message to server: {message}")

        # Receive a response from the server
        response = client_socket.recv(1024).decode()
        print(f"Received response from server: {response}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the socket
        client_socket.close()


if __name__ == "__main__":
    main()
