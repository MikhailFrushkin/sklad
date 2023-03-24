import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import glob
from data.config import path


def generate_choice_menu(message: types.Message, state: FSMContext):
    """вывод клавы сформированной на основе файлов прихода и текущей даты,
     показывает все будущие - 2 дня к текущей дате"""
    menu_choice = ReplyKeyboardMarkup(row_width=1)
    files_ds = glob.glob(f'{path}/*.xlsx')
    df_ds = pd.read_excel('Список поставок с датами.xlsx')

    return menu_choice


menu_first = ReplyKeyboardMarkup(row_width=1)
menu_first.insert(KeyboardButton('Просмотр по объему и кол-ву'))
menu_first.insert(KeyboardButton('Просмотр всех товаров'))
menu_first.insert(KeyboardButton('Просмотр новинок'))


menu_choice_tg = ReplyKeyboardMarkup(row_width=1)
#сбор тг из файла прихода и создание клавы



