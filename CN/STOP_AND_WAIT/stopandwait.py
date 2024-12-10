import time
import random

def stop_and_wait(sender_data):
    for i, data in enumerate(sender_data):
        print(f"Sending Frame {i+1}: {data}")
        ack_received = random.choice([True, False])  # Randomly simulate ack loss
        if ack_received:
            print(f"ACK received for Frame {i+1}")
        else:
            print(f"ACK not received for Frame {i+1}. Resending...")
            time.sleep(1)
            stop_and_wait([data])  # Resend the same frame
        time.sleep(1)  # Simulate delay

# Example usage:
data = ["Frame1", "Frame2", "Frame3"]
stop_and_wait(data)
