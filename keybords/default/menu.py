from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Выбор ячейки')],
    [KeyboardButton('VSL'),
     KeyboardButton('Brak')]], resize_keyboard=True)
