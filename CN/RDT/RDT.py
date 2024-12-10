import time
import random

def unreliable_channel(packet):
    """ Simulate an unreliable network where packets might get lost. """
    if random.choice([True, False]):  
        print(f"Packet {packet['seq']} was lost.")
        return False  
    return True  

# Sender side implementation
def rdt_sender(data):
    """ Implements the reliable data transfer sender using stop-and-wait protocol. """
    seq_num = 0
    for message in data:
        packet = {'seq': seq_num, 'data': message}  
        ack_received = False

        while not ack_received:
            print(f"Sender: Sending Packet {packet['seq']} with data: {packet['data']}")
            if unreliable_channel(packet):
                ack_received = simulate_ack_receiver(packet['seq'])  
            else:
                print(f"Sender: Timeout for Packet {packet['seq']}. Retransmitting...")
                time.sleep(1)  

        seq_num = (seq_num + 1) % 2  

# Receiver side implementation
def simulate_ack_receiver(expected_seq):
    """ Simulates the receiver side for acknowledging packets. """
    ack_lost = random.choice([True, False]) 
    if ack_lost:
        print(f"Receiver: ACK for Packet {expected_seq} was lost.")
        return False
    else:
        print(f"Receiver: ACK received for Packet {expected_seq}.")
        return True

data = ["Frame1", "Frame2", "Frame3", "Frame4", "Frame5"]
rdt_sender(data)
