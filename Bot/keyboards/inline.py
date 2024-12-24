from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder

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
        ],
        [
            KeyboardButton(text='Отправить сообщение всем')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_unregistered_user_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Зарегистрировать'),
            KeyboardButton(text='Изменить удачу')
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
        ],
        [
            KeyboardButton(text='Посмотреть удачу'),
            KeyboardButton(text='Изменить удачу')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True    
)

admin_change_luck_kb = ReplyKeyboardMarkup(
    keyboard=[
       [
            KeyboardButton(text='Задать руками'),
            KeyboardButton(text='Назад')
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
        ],
        [
            KeyboardButton(text='Выбор автомата')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True    
)