import socket

def send_dns_query(domain):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Server address and port
    server_address = ('127.0.0.1', 53)
    
    # Build a simple DNS query
    transaction_id = b'\xaa\xbb'  # Random transaction ID
    flags = b'\x01\x00'  # Standard query
    questions = b'\x00\x01'  # 1 question
    answer_rrs = b'\x00\x00'  # 0 answer RRs
    authority_rrs = b'\x00\x00'  # 0 authority RRs
    additional_rrs = b'\x00\x00'  # 0 additional RRs

    # Convert domain name to DNS query format
    query = b''
    for part in domain.split('.'):
        query += bytes([len(part)]) + part.encode('utf-8')
    query += b'\x00'  # End of domain name
    query_type = b'\x00\x01'  # Type A (host address)
    query_class = b'\x00\x01'  # Class IN (internet)

    dns_query = transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + query + query_type + query_class
    
    # Send the query to the server
    sock.sendto(dns_query, server_address)
    
    # Receive the response from the server
    response, _ = sock.recvfrom(512)
    
    # Close the socket
    sock.close()
    
    # Print the response
    print(f"Received response: {response.hex()}")
    
if __name__ == "__main__":
    send_dns_query('example.com')
