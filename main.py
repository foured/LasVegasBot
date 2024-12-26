import asyncio
from Net.server import Server

from Bot.bot_main import *
from shared import Shared

async def main():
    server = Server()
    Shared.server = server
    server_task = asyncio.create_task(server.run())
    bot_task = asyncio.create_task(bot_main())
    
    await server_task
    await bot_task

if __name__ == '__main__':
    asyncio.run(main())
