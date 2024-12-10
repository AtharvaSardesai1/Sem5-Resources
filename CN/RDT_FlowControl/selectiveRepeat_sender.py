import socket
import time

TIMEOUT = 2
WINDOW_SIZE = 4

def selective_repeat_sender(data, receiver_address):
    base = 0
    next_seq_number = 0
    acked = [False] * len(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    while base < len(data):
        while next_seq_number < base + WINDOW_SIZE and next_seq_number < len(data):
            # Send packet with sequence number
            message = f"{next_seq_number}:{data[next_seq_number]}".encode()
            sock.sendto(message, receiver_address)
            print(f"Sent packet: {message}")
            next_seq_number += 1

        try:
            ack, _ = sock.recvfrom(1024)
            ack = int(ack.decode())
            print(f"Received ACK: {ack}")
            if not acked[ack]:
                acked[ack] = True
                if ack == base:
                    while base < len(data) and acked[base]:
                        base += 1
        except socket.timeout:
            for i in range(base, min(base + WINDOW_SIZE, len(data))):
                if not acked[i]:
                    message = f"{i}:{data[i]}".encode()
                    sock.sendto(message, receiver_address)
                    print(f"Resent packet: {message}")

    sock.close()

# Test the Selective Repeat sender
if __name__ == '__main__':
    receiver_address = ('localhost', 12345)
    data = ["Packet1", "Packet2", "Packet3", "Packet4", "Packet5"]
    selective_repeat_sender(data, receiver_address)
