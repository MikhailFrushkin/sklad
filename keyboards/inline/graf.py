from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

graf_days = InlineKeyboardMarkup(row_width=6)
for i in range(1, 31):
    graf_days.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))
graf_days.insert(InlineKeyboardButton(text='В главное меню', callback_data='exit'))

graf_check = InlineKeyboardMarkup(row_width=2)
graf_check.insert(InlineKeyboardButton(text='По дням', callback_data='days'))
graf_check.insert(InlineKeyboardButton(text='В главное меню', callback_data='exit'))

