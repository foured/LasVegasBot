from Bot.state_machine.state import State, StateBundle
from Bot.state_machine.state_tree import StateTree
from aiogram.types import Message
from Bot.keyboards.inline import *
from shared import Shared

class RegisteredMainMenu(State):
    def __init__(self, tree: StateTree) -> None:
        super().__init__('registered_main_menu', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        await self.tree.user.bot.send_message(
            chat_id=self.tree.user.id,
            text='Вы в меню',
            reply_markup=registered_main_menu
        )
        await self.send_menu()

    async def disable(self) -> None:
        pass

    async def process_message(self, message: Message) -> None:
        from Bot.models.user import UserSubstate

        text = message.text
        if text == 'Баланс':
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Ваш баланс: 💰<b>{self.tree.user.data.money}</b>. Ого!\nДля его пополнения пройдите на кассу.',
                parse_mode='HTML'
            )
            await self.send_menu()

        elif text == 'Код':
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Ваш код: 🔑<b>{self.tree.user.data.code}</b>',
                parse_mode='HTML'
            )
            await self.send_menu()
        elif text == 'Выбор автомата':
            if self.tree.user.substate == UserSubstate.AFK:
                await self.tree.set_state_by_name('choose_slot_state')
            else:
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Вы уже играете',
                    reply_markup=registered_main_menu
                ) 

        else:
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Неисвестная команда',
                reply_markup=registered_main_menu
            )

    async def send_menu(self):
        await self.tree.user.bot.send_message(
            chat_id=self.tree.user.id,
            text='Для дальнейших взаимодействий жмите на кнопки.',
            reply_markup=registered_main_menu
        )

class ChooseSlotState(State):
    def __init__(self, tree: 'StateTree') -> None:
        super().__init__('choose_slot_state', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        free = Shared.server.get_free_machines_ids()
        if len(free) == 0:
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text='Сейчас нет свобобных автоматов.',
            )
            await self.tree.set_state_by_name('registered_main_menu')

        else:
            machines_keyboard_builder = ReplyKeyboardBuilder()
            for i in range(0, len(free), 3):
                row = free[i:i+3]
                machines_keyboard_builder.row(*[KeyboardButton(text=str(fid)) for fid in row])
            machines_keyboard_builder.button(text='Назад')

            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text='Выберите автомат',
                reply_markup=machines_keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
            )


    async def disable(self) -> None:
        pass

    async def process_message(self, message: Message) -> None:
        from Bot.models.user import UserSubstate

        text = message.text.lower()
        if text == 'назад':
            await self.tree.set_state_by_name('registered_main_menu')
        elif text.isdigit():
            fid = int(text)
            if Shared.server.check_free(fid):
                from Net.pockets import UserConnection
                from Net.connection import MachineState

                user = self.tree.user
                pocket = UserConnection(user.data.code, user.data.money, user.winchance,)
                connection = Shared.server.get_connectin(fid)
                connection.writer.write(pocket.to_bytearray())
                connection.state = MachineState.BUSY
                await connection.writer.drain()
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text='Автомат активирован',
                )
                self.tree.user.substate = UserSubstate.PLAYING
                await self.tree.set_state_by_name('registered_main_menu')
            else:
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Автомат с таким номером не активен или не существует',
                )
                await self.enable()

        else:
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Неисвестная команда',
            )
            await self.enable()