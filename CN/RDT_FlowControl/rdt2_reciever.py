import socket

def rdt_2_0_receive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    sock.bind(server_address)
    
    print("Waiting to receive data...")
    while True:
        data, address = sock.recvfrom(4096)
        checksum, payload = data.decode().split(':', 1)
        
        # Check for errors
        calculated_checksum = str(sum(bytearray(payload.encode())) % 256)
        if checksum == calculated_checksum:
            print(f"Received: {payload}")
            sock.sendto('ACK'.encode(), address)
        else:
            print("Checksum error")
            sock.sendto('NAK'.encode(), address)

if __name__ == '__main__':
    rdt_2_0_receive()
