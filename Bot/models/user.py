from aiogram import Bot
from aiogram.types import Message
from state_machine.state_tree import StateTree

from state_machine.states.unregistered import *
from state_machine.states.admin import *
from state_machine.states.registered import *

import enum

class UserRights(enum.Enum):
    USER = 0,
    ADMIN = 1,
    UNREGISTERED = 2

class UserData():
    code: int
    money: int = 0

class User():
    def __init__(self, id: str, bot: Bot) -> None:
        self.id = id
        self.bot = bot
        self.data = UserData()
        self.tree = StateTree(self)
        self.rights = UserRights.UNREGISTERED

    async def setup_unregistered(self):
        self.rights = UserRights.UNREGISTERED
        self.tree.clear()
        uw = UnregisteredWelcome(self.tree)
        self.tree.add_state(uw)

    async def setup_user(self):
        self.rights = UserRights.USER
        self.tree.clear()
        reged_user_w = RegisteredMainMenu(self.tree)
        self.tree.add_state(reged_user_w)

    async def setup_admin(self):
        self.rights = UserRights.ADMIN
        self.tree.clear()
        amm = AdminMainMenu(self.tree)
        reg_user = FindUser(self.tree)
        edit_unreg_user = EditUnregisteredUser(self.tree)
        self.tree.add_state(amm)
        self.tree.add_state(reg_user)
        self.tree.add_state(edit_unreg_user)

    async def process_message(self, message: Message):
        await self.tree.execute_current_state(message)

    async def enable_first_state(self) -> None:
        await self.tree.states[0].enable()