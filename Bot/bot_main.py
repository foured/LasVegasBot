import asyncio

from aiogram import Bot, Dispatcher
from handlers import user_commands
from models.db import DB

async def main():
    bot = Bot('7561117864:AAF4hh7IZ_zHIIvI4OULfGk6k_FrOhILNWU')
    dp = Dispatcher()
    DB.initialize(bot)
    await DB.load()
    dp.include_routers(
        user_commands.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Bot is running.")
    asyncio.run(main())