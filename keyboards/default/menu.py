from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🆚 V-Sales_825'),
     KeyboardButton('☣ R12_BrakIn_825')],
    [KeyboardButton('🤖 Qrcode ячейки')],
    [KeyboardButton('📦 Содержимое ячейки'),
     KeyboardButton('🔍 Поиск на складе')],
    [KeyboardButton('ℹ Информация')]
], resize_keyboard=True)

second_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Назад')],
], resize_keyboard=True)

menu_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🆚 V-Sales_825'),
     KeyboardButton('☣ R12_BrakIn_825')],
    [KeyboardButton('🤖 Qrcode ячейки')],
    [KeyboardButton('📦 Содержимое ячейки'),
     KeyboardButton('🔍 Поиск на складе')],
    [KeyboardButton('ℹ Информация')],
    [KeyboardButton('Загрузка базы')]
], resize_keyboard=True)

dowload_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('012_825'),
     KeyboardButton('A11_825'),
     KeyboardButton('RDiff')],
    [KeyboardButton('Назад')],
], resize_keyboard=True)
