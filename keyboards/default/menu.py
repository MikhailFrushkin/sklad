from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('V-Sales_825'),
     KeyboardButton('R12_BrakIn_825')],
    [KeyboardButton('Показать артикул')]
    ], resize_keyboard=True)