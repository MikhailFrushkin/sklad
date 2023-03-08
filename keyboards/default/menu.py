from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(row_width=2)
menu.insert(KeyboardButton('🆚V-Sales_825'))
menu.insert(KeyboardButton('🗃011_825-Exit_sklad'))
menu.insert(KeyboardButton('🤖Qrcode ячейки'))
menu.insert(KeyboardButton('📖Любой текст в Qr'))
menu.insert(KeyboardButton('📦Содержимое ячейки'))
menu.insert(KeyboardButton('🔍Поиск по наименованию'))
menu.insert(KeyboardButton('📝Проверка товара'))
menu.insert(KeyboardButton('📑Проверка единичек'))
menu.insert(KeyboardButton('💳Акции'))
menu.insert(KeyboardButton('ℹИнформация'))
menu.insert(KeyboardButton('Телефоны'))

second_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('В главное меню')],
], resize_keyboard=True)

menu_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('🆚V-Sales_825'), KeyboardButton('🗃011_825-Exit_sklad'), KeyboardButton('🤖Qrcode ячейки')],
    [KeyboardButton('📖Любой текст в Qr'),
     KeyboardButton('📦Содержимое ячейки'),
     KeyboardButton('🔍Поиск по наименованию')],
    [KeyboardButton('📝Проверка товара'),
     # KeyboardButton('💰Проданный товар'),
     KeyboardButton('📑Проверка единичек')],
    # KeyboardButton('📟 Мой заказ')],
    [KeyboardButton('💳Акции'),
     KeyboardButton('Телефоны')],
    [KeyboardButton('🤬Новые Рдиффы'),
     KeyboardButton('ℹИнформация')],
    [KeyboardButton('Загрузка базы'),
     KeyboardButton('Отправить')],
    [KeyboardButton('Обновить Акции'),
     KeyboardButton('Сброс единичек')],
    [KeyboardButton('Обновить новые рдиффы'),
     KeyboardButton('Сники мод')]
], resize_keyboard=True)

dowload_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('011_825'),
     KeyboardButton('012_825')],
    [KeyboardButton('A11_825'),
     KeyboardButton('V_Sales')],
    [KeyboardButton('RDiff'),
     KeyboardButton('S_825')],
    [KeyboardButton('В главное меню')],
], resize_keyboard=True)

qr_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('011_825-Exit_sklad'),
     KeyboardButton('011_825-Exit_zal'),
     KeyboardButton('011_825-Exit_Dost')],
    [KeyboardButton('V-Sales_825'),
     KeyboardButton('R12_BrakIn_825'),
     KeyboardButton('011_825-02-01-0')],
    [KeyboardButton('012_825-Dost_int8'),
     KeyboardButton('В главное меню')],
], resize_keyboard=True)

orders = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Мой заказ'),
                                        KeyboardButton('Удалить заказ')],
                                       [KeyboardButton('Отправить Мишке'),
                                        KeyboardButton('В главное меню')],
                                       ], resize_keyboard=True)
