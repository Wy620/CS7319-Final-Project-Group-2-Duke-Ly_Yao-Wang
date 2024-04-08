import socket
import json

import socket
import json
import time
import sys

class p2p:


    def __init__(self, ip_address="127.0.0.1", invite_code="test123"):
        self.ip_address = ip_address
        self.invite_code = invite_code
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_started = False
        self.connected = False

        self.HEADER_SIZE = 10  # Adjust as needed

    def start_server(self):
        try:
            port = self.derive_port_from_code(self.invite_code)
            self.socket.bind(('0.0.0.0', port))
            self.socket.listen(1)
            self.server_started = True
            self.connected = True
            print(f"Server started on {self.ip_address}:{port}")
        except socket.error as e:
            print(f"Failed to start server: {e}")

    def connect(self):
        if self.server_started:
            print("Waiting for peer to connect...")
            self.connection, self.address = self.socket.accept()
            self.connected = True
            print(f"Connected to peer at {self.address}")
        else:
            try:
                port = self.derive_port_from_code(self.invite_code)
                self.socket.connect((self.ip_address, port))
                self.connected = True
                print(f"Connected to server at {self.ip_address}:{port}")
            except socket.error as e:
                print(f"Failed to connect: {e}")

    def derive_port_from_code(self, code):
        # Convert the invite code into a port number (this is just an example)
        return 5000  # Replace with your logic


    def send_data(self, data):
        try:
            serialized_data = json.dumps(data)
            serialized_data = f"{len(serialized_data):<{self.HEADER_SIZE}}" + serialized_data
            if self.server_started:
                self.connection.sendall(serialized_data.encode())
            else:
                self.socket.sendall(serialized_data.encode())
        except socket.error as e:
            print(f"Sending data failed: {e}")

    def receive_data(self):
        full_data = ''
        new_msg = True
        while True:
            if self.server_started:
                received_chunk = self.connection.recv(16)  # Adjust buffer size as needed
            else:
                received_chunk = self.socket.recv(16)  # Adjust buffer size as needed
            if new_msg:
                data_length = int(received_chunk[:self.HEADER_SIZE])
                new_msg = False
            full_data += received_chunk.decode()

            if len(full_data) - self.HEADER_SIZE == data_length:
                break

        try:
            return json.loads(full_data[self.HEADER_SIZE:])
        except json.JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
            return {}

    def disconnect(self):
        """
        Disconnect from the peer.
        """
        try:
            self.connection.close()
            self.socket.close()
            self.connected = False
            print("Disconnected from peer.")
        except socket.error as e:
            print(f"Disconnection error: {e}")

    def run_test(self):  # Only for testing
        if len(sys.argv) == 2 and sys.argv[1] == 'server':
            print("Starting server for testing...")
            self.start_server()
            print("Server running. Waiting for connection...")
            self.connect()
            print("Connection established. Exchanging data...")

            # Server receiving and then sending data multiple times
            for i in range(3):  # Number of interactions
                received_data = self.receive_data()
                print(f"Received from client: {received_data}")
                response_data = f"Server response {i + 1}"
                self.send_data(response_data)

        elif len(sys.argv) == 3 and sys.argv[1] == 'client':
            ip_address = sys.argv[2]
            print(f"Connecting to server at {ip_address}...")
            self.ip_address = ip_address
            self.connect()
            print("Connected to server. Exchanging data...")

            # Client sending data first and then receiving server response
            for i in range(3):  # Number of interactions
                send_data = f"Client message {i + 1}"
                self.send_data(send_data)
                received_data = self.receive_data()
                print(f"Received from server: {received_data}")

        else:
            print("Invalid command. Usage:")
            print("  python peer.py server")
            print("  python peer.py client <server_ip>")


if __name__ == "__main__":
    peer = Peer()
    peer.run_test()
