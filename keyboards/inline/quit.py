from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

exitqr = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='Выйти в меню показа артикула', callback_data='exit')
    ]
])
