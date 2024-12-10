import socket
import time
import random

TIMEOUT = 2
WINDOW_SIZE = 4
PACKET_LOSS_PROBABILITY = 0.2  # Probability of dropping a packet (20%)

def go_back_n_sender(data, receiver_address):
    base = 0
    next_seq_number = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    while base < len(data):
        while next_seq_number < base + WINDOW_SIZE and next_seq_number < len(data):
            # Simulate packet loss with some probability
            if random.random() > PACKET_LOSS_PROBABILITY:  # If no packet loss
                message = f"{next_seq_number}:{data[next_seq_number]}".encode()
                sock.sendto(message, receiver_address)
                print(f"Sent packet: {message}")
            else:
                print(f"Packet {next_seq_number} lost")
            
            next_seq_number += 1

        try:
            ack, _ = sock.recvfrom(1024)
            ack = int(ack.decode())
            print(f"Received ACK: {ack}")
            if ack >= base:
                base = ack + 1  # Move the base forward
        except socket.timeout:
            print("Timeout, retransmitting from base")
            next_seq_number = base  # Retransmit from base

    sock.close()

# Test the Go-Back-N sender
if __name__ == '__main__':
    receiver_address = ('localhost', 12345)
    data = ["Packet1", "Packet2", "Packet3", "Packet4", "Packet5"]
    go_back_n_sender(data, receiver_address)
