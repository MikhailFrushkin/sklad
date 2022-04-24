from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mesto1 = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in range(1, 18):
    mesto1.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))
mesto1.insert(InlineKeyboardButton(text='OX', callback_data='012_825-OX'))
mesto1.insert(InlineKeyboardButton(text='RDiff', callback_data='rdiff'))


mesto2 = InlineKeyboardMarkup(row_width=4)
for i in range(1, 9):
    mesto2.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))

mesto3 = InlineKeyboardMarkup(row_width=4)
for i in range(4):
    mesto3.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))

photo = InlineKeyboardMarkup(row_width=1)
photo.add(InlineKeyboardButton(text='Показать фото', callback_data='photo'))

hide = InlineKeyboardMarkup(row_width=1)
hide.add(InlineKeyboardButton(text='Скрыть фото', callback_data='hide'))


search_sklad = InlineKeyboardMarkup(row_width=2)
search_sklad.insert(InlineKeyboardButton(text='012_825', callback_data='012'))
search_sklad.insert(InlineKeyboardButton(text='A11_825', callback_data='a11'))
search_sklad.insert(InlineKeyboardButton(text='Назад', callback_data='exit'))
