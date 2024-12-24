from Bot.models.user import User
from Bot.models.uniq_codes import CodeGenerator
from config import SAVE_FILENAME
from aiogram import Bot
import json
import asyncio
from datetime import datetime

class DB():
    users: list[User] = []
    bot: Bot
    do_log: bool = True

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

    @staticmethod
    def save_to_file(filename: str):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([user.to_dict() for user in DB.users], file, ensure_ascii=False, indent=4)

    @staticmethod
    async def load_from_file(filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                users_data = json.load(file)
                DB.users = [await User.from_dict(data, DB.bot) for data in users_data]
        except FileNotFoundError:
            DB.users = []

    @staticmethod
    def save():
        DB.save_to_file(SAVE_FILENAME)

    @staticmethod
    async def load():
        await DB.load_from_file(SAVE_FILENAME)

    @staticmethod
    async def save_periodically(interval: int):
        while True:
            await asyncio.sleep(interval)
            DB.save()
            if DB.do_log:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"DB saved at {current_time}.")