from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🆚 V-Sales_825'),
     KeyboardButton('☣ R12_BrakIn_825')],
    [KeyboardButton('🤖 Qrcode ячейки')],
    [KeyboardButton('📦 Содержимое ячейки'),
     KeyboardButton('🔍 Поиск на складе')],
    [KeyboardButton('ℹ Информация')]
], resize_keyboard=True)
