import random
import time

MAX_SEGMENTS = 20  
LOSS_PROBABILITY = 0.1 
MAX_CWND = 1000 
MSS = 1  


class TCPSimulator:
    def __init__(self, ssthresh, protocol='reno'):
        self.cwnd = 1  
        self.ssthresh = ssthresh 
        self.duplicate_acks = 0  
        self.protocol = protocol 
        self.segments_sent = 0 
        self.total_acknowledged = 0  
    def send_segment(self):
        self.segments_sent += 1
        if random.random() < LOSS_PROBABILITY:
            print(f"Packet loss detected at segment {self.segments_sent}")
            return False
        else:
            print(f"Segment {self.segments_sent} sent successfully with cwnd = {self.cwnd}")
            return True

    def receive_ack(self):
        if self.send_segment():
            self.duplicate_acks = 0 
            self.total_acknowledged += self.cwnd  
            self.adjust_cwnd_on_ack()
        else:
            self.handle_packet_loss()

    def adjust_cwnd_on_ack(self):
        if self.cwnd < self.ssthresh:
            self.cwnd *= 2
        else:
            if self.protocol == 'aimd' or self.protocol in ['tahoe', 'reno']:
                self.cwnd += 1 

        self.cwnd = min(self.cwnd, MAX_CWND)  

    def handle_packet_loss(self):
        if self.protocol == 'reno' and self.duplicate_acks >= 3:
            print(f"Triple duplicate ACKs detected, fast retransmit at cwnd = {self.cwnd}")
            self.ssthresh = max(self.cwnd // 2, 2)  
            self.cwnd = self.ssthresh  
        else:
            print(f"Timeout or loss detected, resetting cwnd")
            self.ssthresh = max(self.cwnd // 2, 2) 
            self.cwnd = 1  

        self.duplicate_acks = 0 

    def run_simulation(self):
        print(f"Starting TCP {self.protocol.upper()} simulation")
        while self.segments_sent < MAX_SEGMENTS:
            self.receive_ack()
            time.sleep(0.1)  
        print(f"Simulation finished. Total segments sent: {self.segments_sent}")
        print(f"Total acknowledged segments: {self.total_acknowledged}")



def tcp_slow_start():
    print("Simulating TCP Slow Start")
    tcp = TCPSimulator(ssthresh=64, protocol='tahoe')
    tcp.run_simulation()

def tcp_aimd():
    print("Simulating TCP AIMD")
    tcp = TCPSimulator(ssthresh=64, protocol='aimd')
    tcp.run_simulation()

def tcp_tahoe():
    print("Simulating TCP Tahoe")
    tcp = TCPSimulator(ssthresh=64, protocol='tahoe')
    tcp.run_simulation()

def tcp_reno():
    print("Simulating TCP Reno")
    tcp = TCPSimulator(ssthresh=64, protocol='reno')
    tcp.run_simulation()


if __name__ == "__main__":
    tcp_slow_start()
    #tcp_aimd()
    #tcp_tahoe()
    #tcp_reno()
