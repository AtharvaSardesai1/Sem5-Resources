import socket
import time

def rdt_3_0_send(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    sock.settimeout(2)  # Set timeout for retransmission
    
    try:
        # Add checksum to data
        checksum = str(sum(bytearray(data.encode())) % 256)
        packet = f"{checksum}:{data}"
        
        while True:
            print(f"Sending: {packet}")
            sock.sendto(packet.encode(), server_address)
            
            try:
                # Wait for ACK
                response, _ = sock.recvfrom(4096)
                response = response.decode()
                if response == 'ACK':
                    print("Received ACK, transmission successful")
                    break
            except socket.timeout:
                print("Timeout, resending...")
    finally:
        sock.close()

if __name__ == '__main__':
    rdt_3_0_send('Hello, RDT 3.0!')
