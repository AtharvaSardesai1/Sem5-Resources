import random
import time

def transmission(i, N, tf, tt):
    while i <= tf:
        z = 0
        for k in range(i, min(i + N, tf + 1)):
            print(f"Sending Frame {k}...")
            tt[0] += 1
        
        for k in range(i, min(i + N, tf + 1)):
            f = random.randint(0, 1)
            if f == 0:
                print(f"Acknowledgment for Frame {k}...")
                z += 1
            else:
                print(f"Timeout!! Frame Number: {k} Not Received")
                print("Retransmitting Window...")
                break

        print("\n")
        i += z

def main():
    random.seed(time.time())
    
    tf = int(input("Enter the Total number of frames: "))
    N = int(input("Enter the Window Size: "))
    
    tt = [0]  
    i = 1  
    
    transmission(i, N, tf, tt)
    
    print(f"Total number of frames which were sent and resent are: {tt[0]}")

if __name__ == '__main__':
    main()
