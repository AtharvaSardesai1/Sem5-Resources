import time
import random  # Import the random module

def selective_repeat(sender_data, window_size):
    frame_count = len(sender_data)
    base = 0
    next_frame_to_send = 0
    acks = [False] * frame_count

    while base < frame_count:
        # Send frames within the window size
        while next_frame_to_send < base + window_size and next_frame_to_send < frame_count:
            if not acks[next_frame_to_send]:
                print(f"Sending Frame {next_frame_to_send + 1}: {sender_data[next_frame_to_send]}")
            next_frame_to_send += 1

        # Check for acknowledgments
        for i in range(base, min(base + window_size, frame_count)):
            if not acks[i]:
                ack_received = random.choice([True, False])  # Simulate random ack loss
                if ack_received:
                    print(f"ACK received for Frame {i + 1}")
                    acks[i] = True

        # Slide window if base frame is acknowledged
        while base < frame_count and acks[base]:
            base += 1

        time.sleep(1)

# Example usage:
data = ["Frame1", "Frame2", "Frame3", "Frame4", "Frame5"]
selective_repeat(data, window_size=3)
