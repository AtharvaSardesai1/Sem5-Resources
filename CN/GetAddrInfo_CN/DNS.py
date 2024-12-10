import socket

def resolve_domain(domain):
    try:
        results = socket.getaddrinfo(domain, None)
        print(results)
        print(f"IP addresses for {domain}:")
        for result in results:
            ip_address = result[4][0]
            print(ip_address)

    except socket.gaierror:
        print(f"Error: Unable to resolve domain '{domain}'.")

def main():
    domain = input("Enter a domain name: ")
    
    resolve_domain(domain)

if __name__ == "__main__":
    main()
