from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🆚 V-Sales_825'),
     KeyboardButton('☣ R12_BrakIn_825')],
    [KeyboardButton('🤖 Показать Qrcode ячейки')],
    [KeyboardButton('ℹ Информация')]
    ], resize_keyboard=True)
