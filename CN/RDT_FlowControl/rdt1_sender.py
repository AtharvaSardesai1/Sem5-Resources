import socket

def rdt_1_0_send(data):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    
    try:
        # Send data
        print(f"Sending: {data}")
        sent = sock.sendto(data.encode(), server_address)
    finally:
        sock.close()

if __name__ == '__main__':
    rdt_1_0_send('Hello, RDT 1.0!')
