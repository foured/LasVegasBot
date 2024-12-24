from Bot.state_machine.state import State, StateBundle
from Bot.state_machine.state_tree import StateTree
from aiogram.types import Message
from Bot.keyboards.inline import *

import enum

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
        from Bot.models.db import DB
        from Bot.models.user import UserRights

        if message.text == 'Найти пользователя':
            await self.tree.set_state_by_name('admin_find_user')
        elif message.text == 'Посмотреть всех пользователей':
            for user in DB.users:
                user_status = { UserRights.USER: 'Пользователь', UserRights.ADMIN: 'Админ'}.get(user.rights, 'Гость')
                chat = await user.get_chat()
                    
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Пользователь @{chat.username} ({chat.full_name})\n'
                        f'Код: 🔑<b>{user.data.code}</b>\n'
                        f'Статус: 💼<b>{user_status}</b>\n'
                        f'Баланс: 💰<b>{user.data.money}</b>',
                    parse_mode='HTML'
                )
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Выберите опцию',
                reply_markup=admin_main_menu_kb
            )

        elif message.text == 'Отправить сообщение всем':
            await self.tree.set_state_by_name('admin_send_message_to_all')

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
        from Bot.models.user import UserRights
        from Bot.models.db import DB
        from Bot.state_machine.state_tree import StateTree

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
                a_user = await user.get_chat()
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
                    b = StateBundle()
                    b.code = code
                    await self.tree.set_state_by_name('edit_registered_user_edit', b)
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
                text=f'Выберите действие для 🔑<b>{self.code}</b>',
                reply_markup=admin_unregistered_user_menu_kb,
                parse_mode='HTML'
            )  

    async def disable(self) -> None:
        ...

    async def process_message(self, message: Message) -> None:
        from Bot.models.db import DB

        text = message.text
        if text == 'Зарегистрировать':
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Пользователь 🔑<b>{self.code}</b> зарегистрирован.',
                parse_mode='HTML'
            )
            user = DB.get_user_by_code(self.code)
            await self.tree.user.bot.send_message(
                chat_id=user.id,
                text=f'Регистарция пройдена успешно!',
                parse_mode='HTML'
            )
            await user.setup_user()
            await user.enable_first_state()
            await self.tree.set_state_by_name('admin_main_menu')
        
        elif text == 'Изменить удачу':
            bundle = StateBundle()
            bundle.code = self.code
            bundle.return_to = self.name
            await self.tree.set_state_by_name('admin_change_luck', bundle)

        elif text == 'Вернуться в меню':
            await self.tree.set_state_by_name('admin_main_menu')
        else:
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Неизвестная команда',
                reply_markup=admin_unregistered_user_menu_kb,
            )  













class EditRegisteredUser(State):

    class Substate(enum.Enum):
        MENU = 0,
        REPLENISHMENT = 1,
        FORCE_SET = 2

    def __init__(self, tree) -> None:
        super().__init__('edit_registered_user_edit', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        self.substate = EditRegisteredUser.Substate.MENU
        if bundle == None:
            print('Didn`t reciev a bundle in edit_registered_user_edit!')
        self.code = bundle.code
        await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Выберите действие для 🔑<b>{self.code}</b>',
                reply_markup=admin_registered_user_menu_kb,
                parse_mode='HTML'
            )  

    async def disable(self) -> None:
        ...

    async def process_message(self, message: Message) -> None:
        from Bot.models.db import DB

        text = message.text
        if text == 'Пополнить баланс':
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Введите сумму',
                reply_markup=return_to_menu_kb
            )
            self.substate = EditRegisteredUser.Substate.REPLENISHMENT

        elif text == 'Задать баланс':
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Введите сумму',
                reply_markup=return_to_menu_kb
            )
            self.substate = EditRegisteredUser.Substate.FORCE_SET

        elif text == 'Посмотреть удачу':
            user = DB.get_user_by_code(self.code)
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'3 штучки: <b>{user.luck.winchance}</b>\n'
                     f'Джекпот: <b>{user.luck.jackpot}</b>\n'
                     f'Макака: <b>{user.luck.monkey}</b>',
                reply_markup=admin_registered_user_menu_kb,
                parse_mode='HTML'
            ) 

        elif text == 'Изменить удачу':
            bundle = StateBundle()
            bundle.code = self.code
            bundle.return_to = self.name
            await self.tree.set_state_by_name('admin_change_luck', bundle)

        elif text == 'Заблокировать':
            user = DB.get_user_by_code(self.code)
            await self.tree.user.bot.send_message(
                chat_id=user.id,
                text='Ой!',
            )
            await user.setup_unregistered()
            await user.enable_first_state()

            await user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Пользовотель заблокирован',
            ) 

            await self.tree.set_state_by_name('admin_main_menu')

        elif text == 'Назад' or text == 'Вернуться в меню':
            await self.tree.set_state_by_name('admin_main_menu')

        elif self.substate != EditRegisteredUser.Substate.MENU:
            if text.isdigit():
                amount = int(text)
                user = DB.get_user_by_code(self.code)
                if self.substate == EditRegisteredUser.Substate.REPLENISHMENT:
                    user.data.money += amount

                    await user.bot.send_message(
                        chat_id=user.id,
                        text=f'Ваш баланс поплнен на 💰<b>{amount}</b> всего: 💰<b>{user.data.money}</b>',
                        reply_markup=registered_main_menu,
                        parse_mode='HTML'
                    ) 

                else:
                    user.data.money = amount

                    await user.bot.send_message(
                        chat_id=user.id,
                        text=f'Ваш баланс установлен на 💰<b>{amount}</b>',
                        reply_markup=registered_main_menu,
                        parse_mode='HTML'
                    ) 

                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Операция проведена.',
                )

                await self.tree.set_state_by_name('admin_main_menu')

            else:
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Введите корректное число',
                    reply_markup=return_to_menu_kb
                )
        else:
            await self.tree.user.bot.send_message(
                chat_id=self.tree.user.id,
                text=f'Неизвестная команда',
                reply_markup=admin_registered_user_menu_kb,
            )  












class ChangeLuck(State):

    class Substate(enum.Enum):
        MENU = 0,
        INPUT = 1

    def __init__(self, tree):
        super().__init__('admin_change_luck', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        if bundle == None:
            print('Didn`t reciev a bundle in admin_change_luck!')
        self.code = bundle.code
        self.return_to = bundle.return_to
        self.substate = ChangeLuck.Substate.MENU

        await self.tree.user.bot.send_message(
            chat_id=self.tree.user.id,
            text=f'Выберите действие',
            reply_markup=admin_change_luck_kb
        )  

    async def disable(self) -> None:
        pass

    async def process_message(self, message: Message) -> None:
        text = message.text.lower()

        if self.substate == ChangeLuck.Substate.MENU:
            if text == 'задать руками':
                self.substate = ChangeLuck.Substate.INPUT
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Введите данные по шаблону\n(сумма макаки и джекпота: <b>PLACEHOLDER</b>): \n<b>[шанс на 3] [шанс на джекпот] [шанс на макаку]</b>\nПример:',
                    parse_mode='HTML'
                )

                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'0.1 0.1 0.1',
                )

            elif text == 'назад':
                bundle = StateBundle()
                bundle.code = self.code
                await self.tree.set_state_by_name(self.return_to, bundle)

            else:
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Неизвестная команда',
                    reply_markup=admin_change_luck_kb,
                ) 
        else:
            self.substate = ChangeLuck.Substate.MENU
            fs = ChangeLuck.parse_three_floats(text)
            if fs == None:
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Ошибка в введенных данных',
                    reply_markup=admin_change_luck_kb,
                )
            else:
                from Bot.models.user import UserLuck
                from Bot.models.db import DB

                f1, f2, f3 = fs
                user = DB.get_user_by_code(self.code)
                user.luck = UserLuck(f1, f2, f3)
                await self.tree.user.bot.send_message(
                    chat_id=self.tree.user.id,
                    text=f'Данные установлены',
                )
                bundle = StateBundle()
                bundle.code = self.code
                await self.tree.set_state_by_name(self.return_to, bundle)


    def parse_three_floats(input_string: str):
        try:
            parts = input_string.split()
            
            if len(parts) != 3:
                return None
            
            floats = tuple(float(part) for part in parts)
            
            return floats
        except ValueError:
            return None

















class SendMessageToAllMenu(State):
    def __init__(self, tree):
        super().__init__('admin_send_message_to_all', tree)

    async def enable(self, bundle: StateBundle = None) -> None:
        await self.tree.user.bot.send_message(
            chat_id=self.tree.user.id,
            text=f'Введите текст для отправки',
            reply_markup=return_to_menu_kb
        )

    async def disable(self) -> None:
        pass

    async def process_message(self, message: Message) -> None:
        from Bot.models.db import DB

        if message.text != 'Вернуться в меню':
            for user in DB.users:
                await self.tree.user.bot.send_message(
                    chat_id=user.id,
                    text=f'<b>Cообщение:</b> {message.text}',
                    parse_mode='HTML'
                )

        await self.tree.set_state_by_name('admin_main_menu')
