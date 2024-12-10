import socket

def stop_and_wait_receiver():
    expected_sequence_number = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 12345))

    while True:
        packet, addr = sock.recvfrom(1024)
        seq_number, data = packet.decode().split(':')
        seq_number = int(seq_number)
        print(f"Received packet: {packet.decode()}")

        if seq_number == expected_sequence_number:
            print(f"Processing packet: {data}")
            sock.sendto(str(seq_number).encode(), addr)
            print(f"Sent ACK: {seq_number}")
            expected_sequence_number = 1 - expected_sequence_number
        else:
            print("Duplicate packet, sending ACK for the last correct packet")
            sock.sendto(str(1 - expected_sequence_number).encode(), addr)

# Test the Stop-and-Wait receiver
if __name__ == '__main__':
    stop_and_wait_receiver()
