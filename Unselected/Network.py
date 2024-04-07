import socket
from threading import Thread


class Ipv4Checker:
    def get_ipv4_address(self):
        self.s = None
        try:
            # Create a socket object
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Connect to a remote server
            self.s.connect(("8.8.8.8", 80))
            # Get the local IP address of the socket
            ip_address = self.s.getsockname()[0]
            return ip_address
        except socket.error as e:
            print("Error occurred while retrieving IP address:", e)
            return None
        finally:
            # Close the socket
            self.s.close()


class Peer:
    def __init__(self, ip_address, invite_code):
        self.ip_address = ip_address
        self.port = 8080  # Default port is set to 8080
        self.connections = []
        self.accepting_connections = False
        self.connected = False
        self.server_socket = None
        self.invite_code = invite_code
        self.tetris_gui = None

    def connect(self, target_ip_address, invite_code):
        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_connection.connect((target_ip_address, self.port))
        socket_connection.sendall(invite_code.encode())
        response = socket_connection.recv(1024).decode()
        if response == "Accepted":
            print("Connection established with peer")
            self.connections.append(socket_connection)
            self.start_communication(socket_connection)
        else:
            print("Connection refused. Invalid invite code.")
            socket_connection.close()

    def start_accepting_connections(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip_address, self.port))
        self.server_socket.listen()
        self.accepting_connections = True
        print("Listening for incoming connections on port", self.port)
        while self.accepting_connections:
            socket_connection, address = self.server_socket.accept()
            invite_code = socket_connection.recv(1024).decode()
            if invite_code == self.invite_code:
                print("Connection established with peer:", address)
                socket_connection.sendall("Accepted".encode())
                self.connections.append(socket_connection)
                self.start_communication(socket_connection)
            else:
                print("Invalid invite code. Connection refused.")
                socket_connection.sendall("Refused".encode())
                socket_connection.close()

    def start_communication(self, socket_connection):
        def communicate():
            try:
                print("Communication Started")
                while True:
                    received_message = socket_connection.recv(1024).decode("utf-8")
                    if not received_message:
                        break
                    print("Received message from peer", socket_connection.getpeername(), ":", received_message)
                    self.tetris_gui.game.deserialize_from_json(received_message)
                    self.tetris_gui.game.update_view()
                    #self.tetris_gui.draw_piece()
                    #self.tetris_gui.draw_next_shape()
                    #for peer_socket in self.connections:
                        #if peer_socket != socket_connection:
                            #peer_socket.sendall(received_message.encode())

            except Exception as e:
                print("Error reading message from peer:", e)
                self.connections.remove(socket_connection)
                socket_connection.close()

        self.connected = True
        communication_thread = Thread(target=communicate)
        communication_thread.start()

    def send_message(self, message):
        self.send_message_to_all(message)

    def send_message_to_all(self, message):
        for socket_connection in self.connections:
            try:
                socket_connection.sendall(message.encode())
            except Exception as e:
                print("Error sending message to peer:", e)
                self.connections.remove(socket_connection)
                socket_connection.close()

    def stop_accepting_connections(self):
        self.accepting_connections = False
        if self.server_socket:
            self.server_socket.close()
        for socket_connection in self.connections:
            socket_connection.close()
        self.connections.clear()


# Test Usage
"""
if __name__ == "__main__":
    ip_address = input("Enter your IP address: ")
    invite_code = input("Enter the invite code: ")

    peer = Peer(ip_address, invite_code)
    choice = int(input("1. Connect to a peer\n2. Accept incoming connections\nEnter your choice: "))

    if choice == 1:
        target_ip_address = input("Enter target IP address: ")
        peer_invite_code = input("Enter the invite code of the peer: ")
        peer.connect(target_ip_address, peer_invite_code)
    elif choice == 2:
        Thread(target=peer.start_accepting_connections).start()
    else:
        print("Invalid choice")

    while True:
        message = input("Type your message and press enter to send (type 'exit' to quit): ")
        if message.lower() == "exit":
            break
        peer.send_message(message)

    peer.stop_accepting_connections()
"""
