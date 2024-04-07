import socket
import json

import socket
import json
import time
import sys

class Peer:
    def __init__(self, ip_address="127.0.0.1", invite_code="test123"):
        self.ip_address = ip_address
        self.invite_code = invite_code
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_started = False
        self.connected = False

    def start_server(self):
        try:
            port = self.derive_port_from_code(self.invite_code)
            self.socket.bind((self.ip_address, port))
            self.socket.listen(1)
            self.server_started = True
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
        """
        Send game data to the peer.
        :param data: The game data to be sent, expected to be in a serialized format (e.g., JSON).
        """
        try:
            serialized_data = json.dumps(data)
            self.connection.sendall(serialized_data.encode())
        except socket.error as e:
            print(f"Sending data failed: {e}")

    def receive_data(self):
        """
        Receive game data from the peer.
        :return: The game data received from the peer.
        """
        try:
            received_data = self.connection.recv(1024).decode()
            return json.loads(received_data)
        except socket.error as e:
            print(f"Receiving data failed: {e}")
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

    def run_test(self): #only for testing
        if len(sys.argv) == 2 and sys.argv[1] == 'server':
            print("Starting server for testing...")
            self.start_server()
            print("Server running. Waiting for connection...")
            self.connect()
        elif len(sys.argv) == 3 and sys.argv[1] == 'client':
            ip_address = sys.argv[2]
            print(f"Connecting to server at {ip_address}...")
            self.ip_address = ip_address
            self.connect()
        else:
            print("Invalid command. Usage:")
            print("  python peer.py server")
            print("  python peer.py client <server_ip>")

if __name__ == "__main__":
    peer = Peer()
    peer.run_test()
