import json

from aiogram import types
import time
from data.config import path
from database.connect_DB import dbdate
from database.date import *
import random
import sqlite3
import time
from database.connect_DB import *
from database.date import *
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text, italic, code
from loguru import logger

import bot
from all_requests.parse_action import parse_actions, view_actions
from data.config import ADMINS, PASSWORD, path
from database.products import NullProduct
from handlers.users.Verification import verification_start, create_table
from handlers.users.back import back
from handlers.users.cell_content import show_place
from handlers.users.helps import bot_help
from handlers.users.search import search
from handlers.users.show_art import show_art_in_main_menu
from handlers.users.show_qrs import show_qr
from handlers.users.sold_product import read_base_vsl
from handlers.users.stocks_check import start_check_stocks, save_exsel_pst, creat_pst, union_art
from keyboards.default import menu
from keyboards.default.menu import second_menu, menu_admin, dowload_menu
from loader import dp, bot
from state.states import Orders
from state.states import Place, Logging, Messages, QR, Action
from utils.check_bd import check
from utils.open_exsel import dowload
from utils.read_bd import del_orders, mail
import csv
import os

from loguru import logger
from database.date import *
import pandas as pd
from database.connect_DB import *
import peewee
from peewee import *


def read_all_base():
    sklad_list = ['011_825', '012_825', 'A11_825', 'V_Sales', 'RDiff']
    art_dict = {}
    for sklad in sklad_list:
        with open('{}/files/file_old_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Код \nноменклатуры'] in art_dict.keys():
                    art_dict[row['Код \nноменклатуры']].append({
                        row['Местоположение']: row['Физические \nзапасы']
                    })
                else:
                    art_dict[row['Код \nноменклатуры']] = [{
                        row['Местоположение']: row['Физические \nзапасы']
                    }]
    with open('old_base_arts.json', 'w', encoding='utf-8') as file:
        json.dump(art_dict, file, ensure_ascii=False, indent=4)

    art_dict = {}
    for sklad in sklad_list:
        with open('{}/files/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile2:
            reader2 = csv.DictReader(csvfile2)
            for row in reader2:
                if row['Код \nноменклатуры'] in art_dict.keys():
                    art_dict[row['Код \nноменклатуры']].append({
                        row['Местоположение']: row['Физические \nзапасы']
                    })
                else:
                    art_dict[row['Код \nноменклатуры']] = [{
                        row['Местоположение']: row['Физические \nзапасы']
                    }]
    with open('new_base_arts.json', 'w', encoding='utf-8') as file:
        json.dump(art_dict, file, ensure_ascii=False, indent=4)


def new_rdiff():
    rdiff_list = []
    rdiff_list_new = []
    with open('{}/files/file_old_RDiff.csv'.format(path), newline='', encoding='utf-8') as csvfile_old:
        reader_old = csv.DictReader(csvfile_old)
        for row in reader_old:
            rdiff_list.append([row['Код \nноменклатуры'], row['Описание товара'], row['Физические \nзапасы']])
    with open('{}/files/file_RDiff.csv'.format(path), newline='', encoding='utf-8') as csvfile_new:
        reader_new = csv.DictReader(csvfile_new)
        for row2 in reader_new:
            temp = [row2['Код \nноменклатуры'], row2['Описание товара'], row2['Физические \nзапасы']]
            if temp not in rdiff_list:
                rdiff_list_new.append(row2['Код \nноменклатуры'])
    print(rdiff_list_new)
    view_place_rdiff(rdiff_list_new)


def view_place_rdiff(rdiff_list_new):
    with open('new_base_arts.json', 'r', encoding='utf-8') as file:
        data_new = json.load(file)
    with open('old_base_arts.json', 'r', encoding='utf-8') as file:
        data_old = json.load(file)
    data_place = {
    }

    for art in rdiff_list_new:
        try:
            data_place[art] = {}
            if art in data_new.keys():
                data_place[art]['old'] = data_new[art]
            if art in data_old.keys():
                data_place[art]['new'] = data_old[art]
        except KeyError as ex:
            print(art, ex)
    print(data_place)
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data_place, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    read_all_base()
    new_rdiff()
