import socket

def rdt_2_0_send(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    
    try:
        # Add checksum to data
        checksum = str(sum(bytearray(data.encode())) % 256)
        packet = f"{checksum}:{data}"
        print(f"Sending: {packet}")
        sock.sendto(packet.encode(), server_address)
        
        # Wait for ACK/NAK
        response, _ = sock.recvfrom(4096)
        response = response.decode()
        if response == 'ACK':
            print("Received ACK")
        else:
            print("Received NAK, resending...")
            sock.sendto(packet.encode(), server_address)
    finally:
        sock.close()

if __name__ == '__main__':
    rdt_2_0_send('Hello, RDT 2.0!')
