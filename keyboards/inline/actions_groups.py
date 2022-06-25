from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

actions = InlineKeyboardMarkup(row_width=3)
groups_list = [['Декор', '1181'], ['Зеркала', '5359'], ['Ковры', '1184'],
               ['Освещение', '1182'], ['Посуда', '1020'], ['Текстиль', '1140'],
               ['Товары для ванной', '2269'], ['Хозтовары', '1183'], ['Шторы и карнизы', '1185']]
for i in groups_list:
    actions.insert(InlineKeyboardButton(text='{}'.format(i[0]), callback_data='{}'.format(i[1])))
actions.insert(InlineKeyboardButton(text='В главное меню', callback_data='exit'))
