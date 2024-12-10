import socket
import threading
import sys

def receive_messages(client_socket):
    """Function to receive and print messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("Connection to server lost.")
            client_socket.close()
            sys.exit()

def send_messages(client_socket, username):
    """Function to send messages to the server."""
    while True:
        message = input('')
        full_message = f"{username}: {message}"
        client_socket.send(full_message.encode('utf-8'))

def start_client(host='127.0.0.1', port=5555):
    """Function to start the chat client."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input("Enter your username: ")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket, username))
    send_thread.start()

if __name__ == "__main__":
    start_client()
