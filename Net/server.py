import socket
from config import *
from Net.pockets import *
from Net.connection import Connection

class Server():
    def __init__(self):
        self.connections : list[Connection] = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        self.socket.bind(server_address)
        print('Listening on:', server_address)
        self.socket.listen(MAX_CONNECTIONS)

    def run(self):
        try:
            while True:
                client_socket, addr = self.socket.accept()
                con = Connection(self, client_socket, addr)
                print(f'Connected by {addr}')
                con.run()

        except Exception as e:
            print(f'Exception: {e}')
        finally:
            self.socket.close()

    def send_all(self, msg):
        for con in self.connections:
            con.client_socket.sendall(msg)