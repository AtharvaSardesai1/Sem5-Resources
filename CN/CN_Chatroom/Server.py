import socket
import threading

# List to keep track of connected clients
clients = []

def broadcast(message, sender_socket):
    """Function to send a message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    """Function to handle communication with a client."""
    while True:
        try:
            # Receive and broadcast messages
            message = client_socket.recv(1024)
            if message:
                broadcast(message, client_socket)
        except:
            # Remove and close the client socket if an error occurs
            clients.remove(client_socket)
            client_socket.close()
            break

def receive_connections(server_socket):
    """Function to accept and handle incoming client connections."""
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        # Add new client to the list and start a new thread to handle the client
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def start_server(host='127.0.0.1', port=5555):
    """Function to start the chat server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    receive_connections(server_socket)

if __name__ == "__main__":
    start_server()
