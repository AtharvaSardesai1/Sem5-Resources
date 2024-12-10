import socket

WINDOW_SIZE = 4

def selective_repeat_receiver(window_size):
    expected_sequence_number = 0
    received = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 12345))

    while True:
        packet, addr = sock.recvfrom(1024)
        seq_number, data = packet.decode().split(':')
        seq_number = int(seq_number)
        print(f"Received packet: {packet.decode()}")

        if expected_sequence_number <= seq_number < expected_sequence_number + window_size:
            print(f"Storing packet: {data}")
            received[seq_number] = data
            sock.sendto(str(seq_number).encode(), addr)
            print(f"Sent ACK: {seq_number}")
            
            while expected_sequence_number in received:
                print(f"Processing stored packet: {received[expected_sequence_number]}")
                del received[expected_sequence_number]
                expected_sequence_number += 1
        else:
            print("Packet outside window, ignoring")

# Test the Selective Repeat receiver
if __name__ == '__main__':
    selective_repeat_receiver(WINDOW_SIZE)
