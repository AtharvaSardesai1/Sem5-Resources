import sys
import socket

def resolve_hostname_to_ip(hostname):
    try:
        # Perform DNS query to resolve the hostname into an IP address
        ip_address = socket.gethostbyname(hostname)
        print(f"IP address of {hostname} is: {ip_address}")
    except socket.gaierror:
        print(f"Error: Unable to resolve hostname '{hostname}'.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python dns_query.py <hostname>")
        sys.exit(1)
    
    # Get the hostname from the command-line arguments
    hostname = sys.argv[1]
    resolve_hostname_to_ip(hostname)

if __name__ == "__main__":
    main()
