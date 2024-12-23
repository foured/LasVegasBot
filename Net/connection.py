import socket
import json
from config import *

class Connection():
    def __init__(self, server: 'Server', client_socket: socket, addr):
        self.client_socket = client_socket
        self.addr = addr
        self.server = server
        self.authorized = False

    def run(self):
        from Net.server import Server
        try:
            while True:
                data = self.client_socket.recv(BUFFERSIZE)
                if not data:
                    print(f'Client {self.addr} disconnected')
                    break
                self.on_msg(data)

        except Exception as e:
            print(f'Error to handle client: {e}')

        finally:
            self.server.connections.remove(self)
            self.client_socket.close()

    def on_msg(self, data: bytearray):
        from Net.server import Server
        json_data = json.loads(data)
        if json_data['header'] == 'HANDSHAKE':
            self.authorized = True
            self.id = json_data['id']
            for con in self.server.connections:
                if con.id == self.id:
                    print('Warning! Two clients has same id!')

            self.server.connections.append(self)

        
    