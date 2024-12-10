import random
import time

def selective_repeat(i, N, tf, tt):
    ack = [False] * (tf + 1)  
    
    while i <= tf:
        for k in range(i, min(i + N, tf + 1)):
            if not ack[k]:
                print(f"Sending Frame {k}...")
                tt[0] += 1
        
        for k in range(i, min(i + N, tf + 1)):
            if not ack[k]:
                f = random.randint(0, 1)
                if f == 0:
                    print(f"Acknowledgment for Frame {k} received.")
                    ack[k] = True
                else:
                    print(f"Timeout! Frame {k} not received.")
        
        while i <= tf and ack[i]:
            i += 1
        print("\n")
    
def main():
    random.seed(time.time())
    
    tf = int(input("Enter the Total number of frames: "))
    N = int(input("Enter the Window Size: "))
    
    tt = [0]  
    i = 1  
    
    selective_repeat(i, N, tf, tt)
    
    print(f"Total number of frames sent and resent: {tt[0]}")

if __name__ == '__main__':
    main()

