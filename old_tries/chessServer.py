import socket
import threading


def handle_client(conn, addr, opponent_conn):
    print(f"New connection: {addr}")
    while True:
        try:
            # Receive data from the client
            data = conn.recv(1024)
            if not data:
                break  # Connection closed by client

            # Forward the move to the opponent
            print(f"Received move from {addr}: {data.decode()}")
            opponent_conn.sendall(data)

        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break

    conn.close()
    print(f"Connection closed: {addr}")


def chess_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)  # Listen for 2 connections
    print(f"Server listening on {host}:{port}")

    # Accept two connections
    conn1, addr1 = server_socket.accept()
    conn2, addr2 = server_socket.accept()

    # Start a thread to handle each client
    t1 = threading.Thread(target=handle_client, args=(conn1, addr1, conn2))
    t2 = threading.Thread(target=handle_client, args=(conn2, addr2, conn1))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    server_socket.close()


if __name__ == "__main__":
    HOST = '127.0.0.1'  # Standard loopback interface (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    chess_server(HOST, PORT)
