from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🆚 V-Sales_825'),
     KeyboardButton('🗃 011_825-exit_sklad')],
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
     KeyboardButton('🗃 011_825-exit_sklad')],
    [KeyboardButton('🤖 Qrcode ячейки')],
    [KeyboardButton('📦 Содержимое ячейки'),
     KeyboardButton('🔍 Поиск на складе')],
    [KeyboardButton('ℹ Информация')],
    [KeyboardButton('Загрузка базы')]
], resize_keyboard=True)

dowload_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('011_825'),
     KeyboardButton('012_825')],
    [KeyboardButton('A11_825'),
     KeyboardButton('V_Sales')],
    [KeyboardButton('RDiff'),
     KeyboardButton('Назад')],
], resize_keyboard=True)

qr_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('011_825-exit_sklad'),
     KeyboardButton('011_825-exit_zal'),
     KeyboardButton('011_825-exit_Dost')],
    [KeyboardButton('V_Sales_825'),
     KeyboardButton('R12_BrakIn_825')],
    [KeyboardButton('Назад')],
], resize_keyboard=True)
