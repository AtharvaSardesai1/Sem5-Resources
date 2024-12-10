import socket

def handle_client(client_socket):
    # Receive the request from the client
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")
    
    # Prepare a simple HTTP response
    http_response = """\
HTTP/1.1 200 OK

Congrats!!
The http server and http client are connected

"""
    # Send the HTTP response
    client_socket.sendall(http_response.encode('utf-8'))
    
    # Close the connection
    client_socket.close()

def run_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a public host, and a port
    server_socket.bind(('0.0.0.0', 8080))
    
    # Listen for incoming connections (up to 5 clients)
    server_socket.listen(5)
    print("Server listening on port 8080...")
    
    while True:
        # Accept a new client connection
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        
        # Handle the client request
        handle_client(client_socket)

if __name__ == "__main__":
    run_server()
