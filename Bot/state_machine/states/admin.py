from state_machine.state import State, StateBundle
from state_machine.state_tree import StateTree
from aiogram.types import Message
from keyboards.inline import *

class AdminMainMenu(State):
    def __init__(self, tree: StateTree) -> None:
        super().__init__('admin_main_menu', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        await self.tree.user.bot.send_message(
            chat_id=self.tree.user.id,
            text=f'Панель администратора.',
            reply_markup=admin_main_menu_kb
        )
    
    async def disable(self) -> None:
        ...

    async def process_message(self, message: Message) -> None:
        from models.db import DB
        from models.user import UserRights

        if message.text == 'Найти пользователя':
            await self.tree.set_state_by_name('admin_find_user')
        elif message.text == 'Посмотреть всех пользователей':
            for user in DB.users:
                user_status = { UserRights.USER: 'Пользователь', UserRights.ADMIN: 'Админ'}.get(user.rights, 'Гость')
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Пользователь 🔑<b>{user.data.code}</b>\n'
                        f'Статус: 💼<b>{user_status}</b>\n'
                        f'Баланс: 💰<b>{user.data.money}</b>',
                    parse_mode='HTML'
                )
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Выберите опцию',
                reply_markup=admin_main_menu_kb
            )  
        else:
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Неизвестная команда.',
                reply_markup=admin_main_menu_kb
            )   















class FindUser(State):
    def __init__(self, tree: StateTree) -> None:
        super().__init__('admin_find_user', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        await self.tree.user.bot.send_message(
            chat_id=self.tree.user.id,
            text=f'Введите код пользователя.',
            reply_markup=return_to_menu_kb
        )
    
    async def disable(self) -> None:
        ...

    async def process_message(self, message: Message) -> None:
        from models.user import UserRights
        from models.db import DB
        from state_machine.state_tree import StateTree
        text : str = message.text
        if text.isdigit() and 0 <= int(text) <= 999:
            code = int(text)
            user = DB.get_user_by_code(code)
            if user == None:
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Пользователя с таким кодом несуществует. Введите еще раз.',
                    reply_markup=return_to_menu_kb
                )
            else:
                a_user = await self.tree.user.bot.get_chat(user.id)
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Пользователь с кодом 🔑<b>{code}</b> найден: @{a_user.username} ({a_user.full_name})',
                    parse_mode='HTML'
                )
                user_status = { UserRights.USER: 'Пользователь', UserRights.ADMIN: 'Админ'}.get(user.rights, 'Гость')
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Статус пользователя: 💼<b>{user_status}</b>',
                    parse_mode='HTML'
                )
                if user.rights == UserRights.UNREGISTERED:
                    b = StateBundle()
                    b.code = code
                    await self.tree.set_state_by_name('edit_unregistered_user_edit', b)

                elif user.rights == UserRights.USER:
                    ...
                else:
                    await self.tree.user.bot.send_message(
                        chat_id=self.tree.user.id,
                        text=f'Пользователя с таким статусом нельзя изменить',
                        reply_markup=admin_main_menu_kb
                    )


        elif text == 'Вернуться в меню':
            await self.tree.set_state_by_name('admin_main_menu')
        else:
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Введенный код не действителен. Введите еще раз.',
                reply_markup=return_to_menu_kb
            )  












class EditUnregisteredUser(State):
    def __init__(self, tree) -> None:
        super().__init__('edit_unregistered_user_edit', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        if bundle == None:
            print('Didn`t reciev a bundle in edit_unregistered_user_edit!')
        self.code = bundle.code
        await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Выберите действие для 🔑<b>{self.code}</b> (надо будет добавить еще настройки подкрутки удачи)',
                reply_markup=admin_unregistered_user_menu_kb,
                parse_mode='HTML'
            )  

    async def disable(self) -> None:
        ...

    async def process_message(self, message: Message) -> None:
        from models.db import DB
        text = message.text
        if text == 'Зарегистрировать':
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Пользователь 🔑<b>{self.code}</b> зарегистрирован.',
                parse_mode='HTML'
            )
            user = DB.get_user_by_code(self.code)
            await user.setup_user()
            await user.enable_first_state()
            await self.tree.set_state_by_name('admin_main_menu')
              
        elif text == 'Вернуться в меню':
            await self.tree.set_state_by_name('admin_main_menu')