import socket
import struct

# DNS query response template for an A record (IPv4 address)
DNS_RESPONSE_TEMPLATE = b'\x81\x80' + b'\x00\x01' + b'\x00\x01' + b'\x00\x00' + b'\x00\x00'  # Flags, Questions, Answer RRs, Authority RRs, Additional RRs

def create_dns_response(data, ip):
    """
    This function crafts a DNS response packet.
    :param data: The original DNS query packet.
    :param ip: The IP address to respond with.
    :return: DNS response packet.
    """
    # Extract the header from the request
    transaction_id = data[:2]
    flags = DNS_RESPONSE_TEMPLATE
    question_count = data[4:6]
    answer_count = b'\x00\x01'  # Number of answers
    ns_count = b'\x00\x00'
    ar_count = b'\x00\x00'
    
    dns_header = transaction_id + flags + question_count + answer_count + ns_count + ar_count

    # Find the query section and skip it
    query_section_end = data[12:].find(b'\x00') + 13  # 12 is the DNS header size
    query_section = data[12:query_section_end]
    answer_section = query_section + b'\x00\x01\x00\x01'  # Type A (Host Address), Class IN (Internet)

    # TTL (Time to live) and data length
    ttl = struct.pack(">I", 300)  # 300 seconds
    data_len = struct.pack(">H", 4)  # IPv4 is 4 bytes
    
    # Convert the IP to bytes
    ip_parts = ip.split('.')
    ip_bytes = struct.pack("!BBBB", *map(int, ip_parts))
    
    dns_response = dns_header + query_section + answer_section + ttl + data_len + ip_bytes
    return dns_response

def run_dns_server(ip_mapping):
    """
    Runs the DNS server.
    :param ip_mapping: A dictionary mapping domain names to IP addresses.
    """
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to all interfaces on port 53
    sock.bind(('0.0.0.0', 53))
    print("DNS server is running...")

    while True:
        # Receive a DNS query
        data, addr = sock.recvfrom(512)  # DNS messages are typically up to 512 bytes
        print(f"Received DNS query from {addr}")
        
        # Extract the domain name from the query
        domain_name = ''
        query = data[12:]  # Skip the header
        length = query[0]

        while length != 0:
            domain_name += query[1:length+1].decode('utf-8') + '.'
            query = query[length+1:]
            length = query[0]

        # Remove the trailing dot
        domain_name = domain_name[:-1]
        print(f"Query for domain: {domain_name}")

        # Check if the domain name is in our IP mapping
        ip = ip_mapping.get(domain_name, '0.0.0.0')  # Default to 0.0.0.0 if not found

        # Create the DNS response
        response = create_dns_response(data, ip)
        
        # Send the DNS response back to the client
        sock.sendto(response, addr)
        print(f"Sent DNS response with IP: {ip}\n")

if __name__ == "__main__":
    # Map of domain names to IP addresses
    domain_to_ip = {
        'example.com': '93.184.216.34',
        'test.com': '1.2.3.4'
    }
    
    run_dns_server(domain_to_ip)
