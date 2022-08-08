import csv

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import path


def creat_groups_menu():
    verification_btn_groups = InlineKeyboardMarkup(row_width=4)

    with open('{}/utils/file_V_Sales.csv'.format(path), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        groups_list = []
        for row in reader:
            if row['ТГ'] not in groups_list:
                groups_list.append(row['ТГ'])

    for i in sorted(groups_list):
        verification_btn_groups.insert(InlineKeyboardButton(text='{}'.format(i), callback_data='{}'.format(i)))
    verification_btn_groups.insert(InlineKeyboardButton(text='Статистика', callback_data='stat'))
    verification_btn_groups.insert(InlineKeyboardButton(text='В главное меню', callback_data='exit'))
    return verification_btn_groups


verification_view = InlineKeyboardMarkup(row_width=2)
verification_view.insert(InlineKeyboardButton(text='Начать проверку', callback_data='start'))
verification_view.insert(InlineKeyboardButton(text='Весь список', callback_data='all_list'))
verification_view.insert(InlineKeyboardButton(text='Проверенныe', callback_data='tried_list'))
verification_view.insert(InlineKeyboardButton(text='Пропущенные', callback_data='skip_list'))
verification_view.insert(InlineKeyboardButton(text='Не найденные', callback_data='not_found_list'))
verification_view.insert(InlineKeyboardButton(text='Редактировать', callback_data='edided'))
verification_view.insert(InlineKeyboardButton(text='В главное меню', callback_data='exit'))


def verification_check_btn(art):
    verification_check = InlineKeyboardMarkup(row_width=2)
    verification_check.insert(InlineKeyboardButton(text='Да', callback_data='yess{}'.format(art)))
    verification_check.insert(InlineKeyboardButton(text='Нет', callback_data='nooo{}'.format(art)))
    verification_check.insert(InlineKeyboardButton(text='Пропустить', callback_data='skip{}'.format(art)))
    verification_check.insert(InlineKeyboardButton(text='В главное меню', callback_data='exit'))
    return verification_check


verification_edited_status = InlineKeyboardMarkup(row_width=2)
verification_edited_status.insert(InlineKeyboardButton(text='Найден', callback_data='ok'))
verification_edited_status.insert(InlineKeyboardButton(text='Не найден', callback_data='no'))
verification_edited_status.insert(InlineKeyboardButton(text='Пропустить', callback_data='skip_s'))
verification_edited_status.insert(InlineKeyboardButton(text='В главное меню', callback_data='exit'))
