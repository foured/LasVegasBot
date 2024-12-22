from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton
)

return_to_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Вернуться в меню'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Найти пользователя'),
            KeyboardButton(text='Посмотреть всех пользователей')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_unregistered_user_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Зарегистрировать'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True    
)

admin_registered_user_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пополнить баланс'),
            KeyboardButton(text='Задать баланс')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True    
)

registered_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Баланс'),
            KeyboardButton(text='Код')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True    
)