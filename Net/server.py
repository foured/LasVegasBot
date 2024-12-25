import asyncio
from Net.connection import Connection, MachineState
from config import *

class Server():
    def __init__(self):
        self.connections: list[Connection] = []
        self.statistics: int = 0

    async def run(self):
        server = await asyncio.start_server(self.handle_client, HOST, PORT)
        async with server:
            print(f'Listening on {HOST}:{PORT}')
            await server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        connection = Connection(self, reader, writer)
        await connection.run()

    async def send_all(self, msg):
        for con in self.connections:
            con.writer.write(msg)
            await con.writer.drain()

    def get_free_machines_ids(self):
        return [con.id for con in self.connections if con.state == MachineState.FREE]
    
    def check_free(self, id: int) -> bool:
        for con in self.connections:
            if con.id == id and con.state == MachineState.FREE:
                return True
        return False

    def get_connectin(self, id) -> Connection:
        for con in self.connections:
            if con.id == id:
                return con
        return None
