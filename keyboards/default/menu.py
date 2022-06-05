from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🆚 V-Sales_825'),
     KeyboardButton('🗃 011_825-Exit_sklad')],
    [KeyboardButton('🤖 Qrcode ячейки'),
     KeyboardButton('📖 Любой текст в Qr')],
    [KeyboardButton('📦 Содержимое ячейки'),
     KeyboardButton('🔍 Поиск на складах')],
    [KeyboardButton('📝Проверка товара'),
     KeyboardButton('📟 Мой заказ')],
    [KeyboardButton('ℹ Информация')],
], resize_keyboard=True)

second_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Назад')],
], resize_keyboard=True)

menu_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🆚 V-Sales_825'),
     KeyboardButton('🗃 011_825-Exit_sklad')],
    [KeyboardButton('🤖 Qrcode ячейки'),
     KeyboardButton('📖 Любой текст в Qr')],
    [KeyboardButton('📦 Содержимое ячейки'),
     KeyboardButton('🔍 Поиск на складах')],
    [KeyboardButton('📝Проверка товара'),
     KeyboardButton('📟 Мой заказ')],
    [KeyboardButton('ℹ Информация')],
    [KeyboardButton('Загрузка базы'),
     KeyboardButton('mic'),
     KeyboardButton('Отправить')]
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
    [KeyboardButton('011_825-Exit_sklad'),
     KeyboardButton('011_825-Exit_zal'),
     KeyboardButton('011_825-Exit_Dost')],
    [KeyboardButton('V-Sales_825'),
     KeyboardButton('R12_BrakIn_825')],
    [KeyboardButton('Назад')],
], resize_keyboard=True)

orders = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Мой заказ'),
                                        KeyboardButton('Удалить заказ')],
                                       [KeyboardButton('Отправить Мишке'),
                                        KeyboardButton('Назад')],
                                       ], resize_keyboard=True)
