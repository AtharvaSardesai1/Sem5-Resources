import sys
import socket
import webbrowser

def resolve_hostname_to_ip(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"IP address of {hostname} is: {ip_address}")
        return ip_address
    except socket.gaierror:
        print(f"Error: Unable to resolve hostname '{hostname}'.")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python dns_query.py <hostname>")
        sys.exit(1)
    
    hostname = sys.argv[1]
    ip_address = resolve_hostname_to_ip(hostname)
    
    if ip_address:
        # Open the IP address in a web browser
        webbrowser.open(f"http://{ip_address}")

if __name__ == "__main__":
    main()
