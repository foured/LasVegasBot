from models.user import User
from aiogram import Bot
from models.uniq_codes import CodeGenerator

class DB():
    users: list[User] = []
    bot: Bot

    @staticmethod
    async def get_user(id: str) -> User:
        for user in DB.users:
            if user.id == id:
                return user
        user = User(id, DB.bot)
        user.data.code = CodeGenerator.generate_code()
        await user.setup_unregistered()
        DB.users.append(user)
        return user
    
    @staticmethod 
    def get_user_by_code(code: int) -> User:
        for user in DB.users:
            if user.data.code == code:
                return user
        return None

    @staticmethod
    def initialize(bot: Bot) -> None:
        DB.bot = bot
