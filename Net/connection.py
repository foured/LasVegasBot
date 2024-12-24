import asyncio
from config import *
import json
import enum

class MachineState(enum.Enum):
    UNAUTORIZED = 0,
    FREE = 1,
    BUSY = 2

class Connection():
    def __init__(self, server: 'Server', reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.server = server
        self.reader = reader
        self.writer = writer
        self.addr = writer.get_extra_info('peername')
        self.state = MachineState.UNAUTORIZED
        self.id = None
        print(f'Connected by {self.addr}')

    async def run(self):
        try:
            while True:
                data = await self.reader.read(BUFFERSIZE)
                if not data:
                    print(f'Client {self.addr} disconnected')
                    break
                await self.on_msg(data)
            
        except Exception as e:
            print(f'Error handling client {self.addr}: {e}')
        
        finally:
            if self.state != MachineState.UNAUTORIZED:
                self.server.connections.remove(self)
            self.writer.close()
            await self.writer.wait_closed()
    
    async def on_msg(self, data: bytearray):
        json_data = json.loads(data)
        if json_data['header'] == 'HANDSHAKE':
            self.state = MachineState.FREE
            self.id = json_data['id']
            for con in self.server.connections:
                if con.id == self.id:
                    print('Warning! Two clients have the same id!')

            self.server.connections.append(self)
        print(json_data)
