from aiogram import Bot
from aiogram.types import Message

from Bot.state_machine.state_tree import StateTree
from Bot.state_machine.states.unregistered import *
from Bot.state_machine.states.admin import *
from Bot.state_machine.states.registered import *
from Bot.models.uniq_codes import CodeGenerator

from config import ConfigManager

import enum

class UserRights(enum.Enum):
    USER = 0,
    ADMIN = 1,
    UNREGISTERED = 2

class UserSubstate(enum.Enum):
    AFK = 0,
    PLAYING = 1

class UserData:
    def __init__(self, code: int, money: int = 0):
        self.code = code
        self.money = money

    def to_dict(self):
        return {'code': self.code, 'money': self.money}

    @staticmethod
    def from_dict(data):
        return UserData(code=data['code'], money=data.get('money', 0))

class UserLuck:
    def __init__(self, winchance: float, jackpot: float, monkey: float):
        self.winchance: float = winchance
        self.jackpot: float = jackpot
        self.monkey: float = monkey

    def to_dict(self):
        return { 'winchance': self.winchance, 'jackpot': self.jackpot, 'monkey': self.monkey }
    
    @staticmethod
    def from_dict(data):
        return UserLuck(winchance=data['winchance'], jackpot=data['jackpot'], monkey=data['monkey'])

class User():
    def __init__(self, id: str, bot: Bot, data: UserData = None, luck: UserLuck = None, rights: UserRights = UserRights.UNREGISTERED) -> None:
        self.id = id
        self.bot = bot
        self.data = data if data else UserData(-1)
        self.luck = luck if luck else ConfigManager.default_luck()
        self.tree = StateTree(self)
        self.rights = rights
        self.substate = UserSubstate.AFK
    
    async def get_chat(self):
        return await self.bot.get_chat(self.id)

    async def setup_unregistered(self):
        self.rights = UserRights.UNREGISTERED
        self.tree.clear()
        uw = UnregisteredWelcome(self.tree)
        self.tree.add_state(uw)

    async def setup_user(self):
        self.rights = UserRights.USER
        self.tree.clear()
        reged_user_w = RegisteredMainMenu(self.tree)
        select_slot = ChooseSlotState(self.tree)
        self.tree.add_state(reged_user_w)
        self.tree.add_state(select_slot)

    async def setup_admin(self):
        self.rights = UserRights.ADMIN
        self.tree.clear()
        amm = AdminMainMenu(self.tree)
        reg_user = FindUser(self.tree)
        edit_unreg_user = EditUnregisteredUser(self.tree)
        edit_reg_user = EditRegisteredUser(self.tree)
        change_luck = ChangeLuck(self.tree)
        send_to_all = SendMessageToAllMenu(self.tree)
        self.tree.add_state(amm)
        self.tree.add_state(reg_user)
        self.tree.add_state(edit_unreg_user)
        self.tree.add_state(edit_reg_user)
        self.tree.add_state(change_luck)
        self.tree.add_state(send_to_all)

    async def process_message(self, message: Message):
        await self.tree.execute_current_state(message)

    async def enable_first_state(self) -> None:
        await self.tree.states[0].enable()

    def to_dict(self):
        return {
            'id': self.id,
            'data': self.data.to_dict(),
            'luck': self.luck.to_dict(),
            'rights': self.rights.name
        }
    
    @staticmethod
    async def from_dict(data, bot: Bot):
        user_data = UserData.from_dict(data['data'])
        user_luck = UserLuck.from_dict(data['luck'])
        rights = UserRights[data['rights']]
        user = User(id=data['id'], bot=bot, data=user_data, luck=user_luck, rights=rights)
        CodeGenerator.codes.add(user.data.code)
        match user.rights:
            case UserRights.UNREGISTERED:
                await user.setup_unregistered()
            case UserRights.USER:
                await user.setup_user()
            case UserRights.ADMIN:
                await user.setup_admin()
        return user