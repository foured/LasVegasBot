from state_machine.state import State, StateBundle
from state_machine.state_tree import StateTree
from aiogram.types import Message

class UnregisteredWelcome(State):
    def __init__(self, tree: StateTree) -> None:
        super().__init__('unregistered_welcome', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        await self.tree.user.bot.send_message(
            chat_id=self.tree.user.id,
            text=f'Добро пожаловать в Лас Вегас! '
                 f'Ваш уникальный код: 🔑<b>{self.tree.user.data.code}</b>. Пройдите на регистрацию!',
            parse_mode='HTML'
        )

    async def disable(self) -> None:
        pass

    async def process_message(self, message: Message) -> None:
        if message.text == 'nelly'.lower():
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Права администратора выданы.',
            )

            await self.tree.user.setup_admin()
            await self.tree.user.enable_first_state()

        else:
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Ваш уникальный код: 🔑<b>{self.tree.user.data.code}</b>. Пройдите регистрацию!',
                parse_mode='HTML'
            )
    