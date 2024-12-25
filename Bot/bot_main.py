import asyncio

from aiogram import Bot, Dispatcher
from Bot.handlers import user_commands
from Bot.models.db import DB
from shared import Shared

async def bot_main():
    print("Starting bot")
    bot = Bot('7561117864:AAF4hh7IZ_zHIIvI4OULfGk6k_FrOhILNWU')
    Shared.bot = bot
    dp = Dispatcher()
    DB.initialize(bot)
    await DB.load()
    dp.include_routers(
        user_commands.router
    )
    asyncio.create_task(DB.save_periodically(30))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# if __name__ == '__main__':
#     print("Bot is running.")
#     asyncio.run(bot_main())