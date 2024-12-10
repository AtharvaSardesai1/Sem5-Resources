import socket

def run_client():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server (localhost on port 8080)
    client_socket.connect(('127.0.0.1', 8080))
    
    # Prepare an HTTP GET request
    http_request = """\
GET / HTTP/1.1
Host: localhost

"""
    # Send the HTTP request
    client_socket.sendall(http_request.encode('utf-8'))
    
    # Receive the response from the server
    response = client_socket.recv(4096).decode('utf-8')
    print(f"Received response:\n{response}")
    
    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    run_client()
