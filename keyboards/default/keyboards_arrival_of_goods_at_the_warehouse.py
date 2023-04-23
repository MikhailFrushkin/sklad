import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import path


def generate_choice_menu():
    """вывод клавы сформированной на основе файлов прихода и текущей даты,
     показывает все будущие - 2 дня к текущей дате"""
    menu_choice = ReplyKeyboardMarkup(row_width=1)
    list_ds = pd.read_csv(f'{path}/files/file_arrival/keyboards.csv')
    if not list_ds.empty:
        list_ds['union'] = list_ds['Код графика'] + '  ' + \
                           list_ds['Планируемая дата прихода в магазин'].apply(
                               lambda x: pd.to_datetime(x).strftime("%d.%m.%Y")) + \
                           '  ' + list_ds['Тип операции'] + \
                           '  ' + list_ds['Объем'].apply(lambda x: str(x))
        list_ds = list_ds['union'].to_list()
        print(list_ds)
    if list_ds:
        for key in list_ds:
            temp = key.split('  ')
            menu_choice.insert(KeyboardButton(f'{temp[0]} {temp[1]}\n{temp[2]} - {temp[3]} куба'))
    menu_choice.insert(KeyboardButton('В главное меню'))
    return menu_choice


menu_first = ReplyKeyboardMarkup(row_width=1)
menu_first.insert(KeyboardButton('Просмотр по объему и кол-ву'))
menu_first.insert(KeyboardButton('Просмотр всех товаров'))
menu_first.insert(KeyboardButton('Просмотр новинок'))
menu_first.insert(KeyboardButton('Назад'))
menu_first.insert(KeyboardButton('В главное меню'))

menu_arrival = ReplyKeyboardMarkup(row_width=1)
menu_arrival.insert(KeyboardButton('Назад'))
menu_arrival.insert(KeyboardButton('В главное меню'))


def menu_choice_tg(name):
    choice_tg = ReplyKeyboardMarkup(row_width=1)
    df = pd.read_excel(f'{path}/files/file_arrival/result/{name}.xlsx')
    df['SG'] = df['SG'].astype(str)
    list_tg = sorted(df['SG'].unique().tolist())
    for group in list_tg:
        if group != 'nan':
            choice_tg.insert(KeyboardButton(f'{group}'))
        else:
            choice_tg.insert(KeyboardButton('Нет данных о ТГ'))
    choice_tg.insert(KeyboardButton('Назад'))
    choice_tg.insert(KeyboardButton('В главное меню'))
    return choice_tg


def menu_choice_tg_new(name):
    choice_tg = ReplyKeyboardMarkup(row_width=1)
    df = pd.read_excel(f'{path}/files/file_arrival/result/{name}_result_new.xlsx')
    df['ТГ'] = df['ТГ'].astype(str)
    for group in sorted(df['ТГ'].unique().tolist()):
        if group != 'nan':
            choice_tg.insert(KeyboardButton(f'{group}. Артикулов: {len(df[df["ТГ"] == group])}'))
        else:
            choice_tg.insert(KeyboardButton(f'Нет данных о ТГ. Артикулов: {len(df[df["ТГ"] == group])}'))
    choice_tg.insert(KeyboardButton('Назад'))
    choice_tg.insert(KeyboardButton('В главное меню'))
    return choice_tg


if __name__ == '__main__':
    # print(generate_choice_menu())
    print(menu_choice_tg_new('DS12341231222'))
