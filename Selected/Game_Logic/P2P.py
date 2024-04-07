import socket
from threading import Thread
import json

class Peer:
    def __init__(self, ip_address, invite_code):
        self.ip_address = ip_address
        self.port = 8080  # Default port is set to 8080
        self.connections = []
        self.accepting_connections = False
        self.server_socket = None
        self.invite_code = invite_code

        print("IP Address:", self.ip_address)
        print("Invite Code:", self.invite_code)

    def connect(self, target_ip_address, invite_code):
        if target_ip_address != self.ip_address:
            print("Invalid IP address. Connection refused.")
            return

        if invite_code != self.invite_code:
            print("Invalid invite code. Connection refused.")
            return

        try:
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
        except Exception as e:
            print("Error connecting to peer:", e)


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
                    received_message = socket_connection.recv(1024).decode()
                    if not received_message:
                        break
                    print("Received message from peer", socket_connection.getpeername(), ":", received_message)
                    for peer_socket in self.connections:
                        if peer_socket != socket_connection:
                            peer_socket.sendall(received_message.encode())
            except Exception as e:
                print("Error reading message from peer:", e)
                self.connections.remove(socket_connection)
                socket_connection.close()

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

    def send_game_state(self, game_state):
        message = {
            'type': 'game_state',
            'data': game_state
        }
        self.send_message_to_all(json.dumps(message))

    def send_player_action(self, player_action):
        message = {
            'type': 'player_action',
            'data': player_action
        }
        self.send_message_to_all(json.dumps(message))

    def receive_game_message(self, received_message):
        message = json.loads(received_message)
        if message['type'] == 'game_state':
            game_state = message['data']
            # Process received game state
        elif message['type'] == 'player_action':
            player_action = message['data']
            # Process received player action



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