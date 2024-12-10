import socket

def rdt_1_0_receive():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    sock.bind(server_address)
    
    print("Waiting to receive data...")
    while True:
        data, address = sock.recvfrom(4096)
        print(f"Received: {data.decode()}")

if __name__ == '__main__':
    rdt_1_0_receive()
