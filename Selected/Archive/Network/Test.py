import socket

def get_ipv4_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a remote server
        s.connect(("8.8.8.8", 80))
        # Get the local IP address of the socket
        ip_address = s.getsockname()[0]
        return ip_address
    except socket.error as e:
        print("Error occurred while retrieving IP address:", e)
        return None
    finally:
        # Close the socket
        s.close()

if __name__ == "__main__":
    ipv4_address = get_ipv4_address()
    if ipv4_address:
        print("Current IPv4 address:", ipv4_address)
    else:
        print("Failed to retrieve the IPv4 address.")
