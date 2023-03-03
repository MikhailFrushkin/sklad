from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


stocks = InlineKeyboardMarkup(row_width=2)
stocks.insert(InlineKeyboardButton(text='Текстиль', callback_data='11'))
stocks.insert(InlineKeyboardButton(text='Ванная комната', callback_data='20'))
stocks.insert(InlineKeyboardButton(text='Шторы', callback_data='21'))
stocks.insert(InlineKeyboardButton(text='Посуда', callback_data='22'))
stocks.insert(InlineKeyboardButton(text='Декор', callback_data='23'))
stocks.insert(InlineKeyboardButton(text='Химия, хранение, ковры', callback_data='28'))
stocks.insert(InlineKeyboardButton(text='Прихожая', callback_data='35'))
stocks.insert(InlineKeyboardButton(text='Свет', callback_data='25'))
stocks.insert(InlineKeyboardButton(text='Мебель', callback_data='ebel'))
stocks.insert(InlineKeyboardButton(text='Выгрузить файлом', callback_data='files'))
# stocks.insert(InlineKeyboardButton(text='Мин.витрина', callback_data='min'))
stocks.insert(InlineKeyboardButton(text='Выход', callback_data='exit'))

choise_num = InlineKeyboardMarkup(row_width=3)
choise_num.insert(InlineKeyboardButton(text='0', callback_data='zero'))
choise_num.insert(InlineKeyboardButton(text='1-3', callback_data='low'))
choise_num.insert(InlineKeyboardButton(text='4-10', callback_data='norm'))
choise_num.insert(InlineKeyboardButton(text='Выход', callback_data='exit'))


choise = InlineKeyboardMarkup(row_width=2)
choise.insert(InlineKeyboardButton(text='Да', callback_data='yes'))
choise.insert(InlineKeyboardButton(text='Нет', callback_data='no'))

