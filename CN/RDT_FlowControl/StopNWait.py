# Global variables to track states
timer = 0
wait_for_ack = -1
frameQ = 0
cansend = 1
t = 0

# Sender function simulating frame transmission
def sender(i, frame):
    global wait_for_ack, frameQ, cansend, timer, t
    wait_for_ack += 1

    if wait_for_ack == 3:
        if i == frame[t]:
            frameQ += 1
            t += 1

        if frameQ == 0:
            print(f"NO FRAME TO SEND at time = {i}")
        elif frameQ > 0 and cansend == 1:
            print(f"FRAME SENT at time = {i}")
            cansend = -1
            frameQ -= 1
            timer += 1
            print(f"Timer in sender = {timer}")
        elif frameQ > 0 and cansend == -1:
            print(f"FRAME IN QUEUE FOR TRANSMISSION at time = {i}")

        if frameQ > 0:
            t += 1

    print(f"Frame Queue = {frameQ}")
    print(f"Current time = {i}, Frame index = {t}")
    if t < len(frame):
        print(f"Value in frame[{t}] = {frame[t]}")

# Receiver function simulating acknowledgment
def recv(i):
    global timer, wait_for_ack

    print(f"Timer in receiver = {timer}")
    if timer > 0:
        timer += 1
    if timer == 3:
        print(f"FRAME ARRIVED at time = {i}")
        wait_for_ack = 0
        timer = 0
    else:
        print(f"WAITING FOR FRAME at time = {i}")

# Main function
def main():
    frame = list(range(5))  # Initialize an array for frames [0, 1, 2, 3, 4]

    print("Simulation of frame transmission over time:")
    for j in range(3):
        print(f"\nTime = {j}:")
        sender(j, frame)
        recv(j)

# Run the main function
if __name__ == '__main__':
    main()
