import random

# Function simulating the selective repeat protocol
def receiver(tmp1):
    # Randomly simulates successful frame reception
    return random.randint(0, tmp1)

def negack(tmp1):
    # Randomly simulates negative acknowledgment (NACK)
    return random.randint(0, tmp1)

def simulate(windowsize):
    # Simulates sending frames within the window size
    return random.randint(1, windowsize)

# Main function
def main():
    windowsize = 4
    no_of_packet = random.randint(5, 10)  # Number of packets to send (randomly chosen between 5 and 10)
    more_packet = no_of_packet
    tmp4 = 0  # Tracks the number of successfully sent frames

    print(f"Number of frames is: {no_of_packet}")

    while more_packet > 0:
        tmp1 = simulate(windowsize)  # Simulate how many frames we can send in the current window
        windowsize -= tmp1  # Reduce window size by the number of frames sent
        tmp4 += tmp1  # Track sent frames

        if tmp4 > no_of_packet:
            tmp4 = no_of_packet  # Avoid sending more than the available packets

        for i in range(no_of_packet - more_packet, tmp4):
            print(f"\nSending Frame {i + 1}")

        # Simulate receiving acknowledgment for the sent frames
        tmp2 = receiver(tmp1)
        tmp3 = tmp2  # Number of acknowledged frames

        if tmp3 > no_of_packet:
            tmp3 = no_of_packet  # Avoid acknowledging more than available packets

        # Simulate negative acknowledgment (NACK) or frame loss
        tmp2 = negack(tmp1)

        if tmp2 != 0:
            # If NACK or frame lost, retransmit the frame
            print(f"\nNo acknowledgement for the frame {tmp2}")
            print(f"Retransmitting frame {tmp2}")

        more_packet -= tmp1  # Decrease remaining packets by the number of successfully sent frames

        if windowsize <= 0:
            windowsize = 4  # Reset window size after the transmission window is exhausted

    print("\nSelective Repeat Protocol Ends. All packets are successfully transmitted.")

# Run the main function
if __name__ == '__main__':
    main()
