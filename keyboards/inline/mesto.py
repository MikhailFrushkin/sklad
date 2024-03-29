from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mesto1 = InlineKeyboardMarkup(row_width=4)
for i in range(1, 18):
    mesto1.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))
mesto1.insert(InlineKeyboardButton(text='OX', callback_data='012_825-OX'))
mesto1.insert(InlineKeyboardButton(text='Dost_int', callback_data='dost'))
mesto1.insert(InlineKeyboardButton(text='RDiff', callback_data='rdiff'))


mesto2 = InlineKeyboardMarkup(row_width=4)
for i in range(1, 9):
    mesto2.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))

mesto3 = InlineKeyboardMarkup(row_width=5)
for i in range(5):
    mesto3.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))

photo = InlineKeyboardMarkup(row_width=1)
photo.add(InlineKeyboardButton(text='Показать фото', callback_data='photo'))

hide = InlineKeyboardMarkup(row_width=1)
hide.add(InlineKeyboardButton(text='Скрыть фото', callback_data='hide'))


search_sklad_b = InlineKeyboardMarkup(row_width=2)
search_sklad_b.insert(InlineKeyboardButton(text='012_825', callback_data='012_825'))
search_sklad_b.insert(InlineKeyboardButton(text='V_Sales', callback_data='V_Sales'))
search_sklad_b.insert(InlineKeyboardButton(text='На всех складах', callback_data='all'))
search_sklad_b.insert(InlineKeyboardButton(text='Поиск по названию', callback_data='name'))

