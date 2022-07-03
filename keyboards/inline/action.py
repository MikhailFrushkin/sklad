from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

product_num = InlineKeyboardMarkup(row_width=3)

product_num.insert(InlineKeyboardButton(text='5', callback_data='5'))
product_num.insert(InlineKeyboardButton(text='10', callback_data='10'))
product_num.insert(InlineKeyboardButton(text='20', callback_data='20'))
product_num.insert(InlineKeyboardButton(text='Выход', callback_data='exit'))
