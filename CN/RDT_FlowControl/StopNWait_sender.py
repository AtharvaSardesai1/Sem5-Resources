import socket
import time

TIMEOUT = 2  # Timeout duration in seconds

def stop_and_wait_sender(data, receiver_address):
    sequence_number = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    for packet in data:
        while True:
            # Send packet with sequence number
            message = f"{sequence_number}:{packet}".encode()
            sock.sendto(message, receiver_address)
            print(f"Sent packet: {message}")

            try:
                ack, _ = sock.recvfrom(1024)
                ack = int(ack.decode())
                print(f"Received ACK: {ack}")

                if ack == sequence_number:
                    break  # ACK received, send the next packet
            except socket.timeout:
                print("Timeout, retransmitting...")
                continue  # Timeout, retransmit packet

        sequence_number = 1 - sequence_number  # Flip between 0 and 1

    sock.close()

# Test the Stop-and-Wait sender
if __name__ == '__main__':
    receiver_address = ('localhost', 12345)
    data = ["Packet1", "Packet2", "Packet3"]
    stop_and_wait_sender(data, receiver_address)
