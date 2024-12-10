import sys
import subprocess
import webbrowser

def perform_nslookup(hostname):
    try:
        result = subprocess.run(['nslookup', hostname], capture_output=True, text=True, check=True)
        
        # Print the output from nslookup
        print(result.stdout)

        # Extract the IP address or domain from the nslookup result (optional for more complex parsing)
        ip_address = None
        for line in result.stdout.splitlines():
            if 'Address:' in line and 'Server' not in line:
                ip_address = line.split(':')[-1].strip()
                break
        
        return ip_address

    except subprocess.CalledProcessError as e:
        print(f"Error performing nslookup for {hostname}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Check if the number of command-line arguments is not equal to 2
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <hostname>", file=sys.stderr)
        sys.exit(1)  # Terminate with failure status
    
    # Copy the hostname from the command-line argument
    hostname = sys.argv[1]
    
    # Perform nslookup on the hostname
    ip_address = perform_nslookup(hostname)
    
    if ip_address:
        # Open the hostname or IP address in the default web browser
        url = f"https://{ip_address}"
        print(f"Opening {url} in the web browser...")
        webbrowser.open(url)
    else:
        print("Could not determine the IP address.")

if __name__ == "__main__":
    main()
