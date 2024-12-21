import socket

HOST = '127.0.0.1'
PORT = 65432

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address =(HOST, PORT)
socket.bind(server_address)

print('listening on:', server_address)
socket.listen(1)

while True:
    connection, client_address = socket.accept()

    with connection:

        while True:
            data = connection.recv(16)
            if not data:
                break
            print(f"Получено: {data.decode()}")
            connection.sendall(b'1')
