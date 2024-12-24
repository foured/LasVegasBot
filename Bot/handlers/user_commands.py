from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from Bot.models.db import DB
from Bot.models.user import User

db = DB()

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    user = await DB.get_user(message.from_user.id)
    await user.enable_first_state()

@router.message()
async def on_message(message: Message):
    user = await DB.get_user(message.from_user.id)
    await user.process_message(message)