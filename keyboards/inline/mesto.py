from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mesto1 = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in range(1, 18):
    mesto1.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))

mesto2 = InlineKeyboardMarkup(row_width=4)
for i in range(1, 9):
    mesto2.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))

mesto3 = InlineKeyboardMarkup(row_width=4)
for i in range(4):
    mesto3.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))
