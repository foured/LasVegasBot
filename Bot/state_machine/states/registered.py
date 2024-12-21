from state_machine.state import State, StateBundle
from state_machine.state_tree import StateTree
from aiogram.types import Message
from keyboards.inline import *

class RegisteredMainMenu(State):
    def __init__(self, tree: StateTree) -> None:
        super().__init__('registered_main_menu', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        await self.tree.user.bot.send_message(
            chat_id=self.tree.user.id,
            text='Регистарция пройдена успешно!',
        )
        await self.send_menu()

    async def disable(self) -> None:
        pass

    async def process_message(self, message: Message) -> None:
        text = message.text
        if text == 'Баланс':
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Ваш баланс: 💰<b>{self.tree.user.data.money}</b>. Ого!\n Для его пополнения пройдите на кассу.',
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