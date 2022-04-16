from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🆚 V-Sales_825'),
     KeyboardButton('☣ R12_BrakIn_825')],
    [KeyboardButton('🤖 Показать Qrcode ячейки'),
     KeyboardButton('📦 Содержимое ячейки')],
    [KeyboardButton('ℹ Информация'),
     KeyboardButton('Мой график(в разработке)')]
    ], resize_keyboard=True)
