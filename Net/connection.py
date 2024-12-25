import asyncio
from config import *
import json
import enum
from Net.pockets import *

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
        from Bot.models.db import DB
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
        print(json_data)
        if json_data['header'] == 'HANDSHAKE':
            self.state = MachineState.FREE
            self.id = json_data['id']
            for con in self.server.connections:
                if con.id == self.id:
                    print('Warning! Two clients have the same id!')

            self.server.connections.append(self)
        elif self.state != MachineState.UNAUTORIZED and json_data['header'] == 'USER_RESULT':
            from Bot.models.db import DB
            from shared import Shared
            from Bot.keyboards.inline import registered_main_menu
            from Bot.models.user import UserSubstate

            user_res = UserResult.from_json(data)
            self.state = MachineState.FREE
            user = DB.get_user_by_code(user_res.code)
            user.data.money = user_res.end
            user.substate = UserSubstate.AFK
            mres = user_res.end - user_res.start
            self.server.statistics += mres
            await Shared.bot.send_message(
                chat_id=user.id,
                text=f'Результат вашей игры: {mres}',
                parse_mode='HTML'
            )
            await Shared.bot.send_message(
                chat_id=user.id,
                text=f'Ваш баланс: 💰<b>{user.data.money}</b>. Ого!\nДля его пополнения пройдите на кассу.',
                parse_mode='HTML',
                reply_markup=registered_main_menu
            )
