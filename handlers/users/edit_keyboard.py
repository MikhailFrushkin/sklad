import csv
import os

from loguru import logger
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.connect_DB import *
import peewee
from peewee import *

from data.config import path
from database.users import Users, Keyboard

myfile = '{}/database/mydatabase.db'.format(path)


KeyboardButton('🆚V-Sales_825')
KeyboardButton('🗃011_825-Exit_sklad')
KeyboardButton('🤖Qrcode ячейки')
KeyboardButton('📖Любой текст в Qr')
KeyboardButton('📦Содержимое ячейки')
KeyboardButton('🔍Поиск по наименованию')
KeyboardButton('📝Проверка товара')
KeyboardButton('💰Проданный товар')
KeyboardButton('📑Проверка единичек')
KeyboardButton('💳Акции')
KeyboardButton('ℹИнформация')
KeyboardButton('Телефоны')


def create_keyboard(id_user):
    try:
        dbhandle.connect()
        query = Users.get(Users.id_tg == id_user)
        menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        if query.keyboard.vsales:
            menu.insert(KeyboardButton('🆚V-Sales_825'))
        if query.keyboard.ex_sklad:
            menu.insert(KeyboardButton('🗃011_825-Exit_sklad'))
        if query.keyboard.qr_cell:
            menu.insert(KeyboardButton('🤖Qrcode ячейки'))
        if query.keyboard.text_qr:
            menu.insert(KeyboardButton('📖Любой текст в Qr'))
        if query.keyboard.content:
            menu.insert(KeyboardButton('📦Содержимое ячейки'))
        if query.keyboard.search:
            menu.insert(KeyboardButton('🔍Поиск по наименованию'))
        if query.keyboard.check:
            menu.insert(KeyboardButton('📝Проверка товара'))
        if query.keyboard.buy:
            menu.insert(KeyboardButton('💰Проданный товар'))
        if query.keyboard.check_one:
            menu.insert(KeyboardButton('📑Проверка единичек'))
        if query.keyboard.stock:
            menu.insert(KeyboardButton('💳Акции'))
        if query.keyboard.info:
            menu.insert(KeyboardButton('ℹИнформация'))
        if query.keyboard.tel:
            menu.insert(KeyboardButton('Телефоны'))
        dbhandle.close()
        if len(menu['keyboard']) == 0:
            menu.insert(KeyboardButton('В главное меню'))
    except Exception as ex:
        logger.debug(ex)
    finally:
        dbhandle.close()
    return menu


def inlane_edit_keyboard(id_user):
    try:
        dbhandle.connect()
        query = Users.get(Users.id_tg == id_user)
        menu_inlane = InlineKeyboardMarkup(row_width=2)
        if query.keyboard.vsales:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 🆚V-Sales_825', callback_data='vsales'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 🆚V-Sales_825', callback_data='vsales'))

        if query.keyboard.ex_sklad:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 🗃011_825-Exit_sklad', callback_data='ex_sklad'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 🗃011_825-Exit_sklad', callback_data='ex_sklad'))

        if query.keyboard.qr_cell:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 🤖Qrcode ячейки', callback_data='qr_cell'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 🤖Qrcode ячейки', callback_data='qr_cell'))

        if query.keyboard.text_qr:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 📖Любой текст в Qr', callback_data='text_qr'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 📖Любой текст в Qr', callback_data='text_qr'))

        if query.keyboard.content:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 📦Содержимое ячейки', callback_data='content'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 📦Содержимое ячейки', callback_data='content'))

        if query.keyboard.search:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 🔍Поиск по наименованию', callback_data='search'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 🔍Поиск по наименованию', callback_data='search'))

        if query.keyboard.check:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 📝Проверка товара', callback_data='check'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 📝Проверка товара', callback_data='check'))

        if query.keyboard.buy:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 💰Проданный товар', callback_data='buy'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 💰Проданный товар', callback_data='buy'))

        if query.keyboard.check_one:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 📑Проверка единичек', callback_data='check_one'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 📑Проверка единичек', callback_data='check_one'))

        if query.keyboard.stock:
            menu_inlane.insert(InlineKeyboardButton(text='✅ 💳Акции', callback_data='stock'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ 💳Акции', callback_data='stock'))

        if query.keyboard.info:
            menu_inlane.insert(InlineKeyboardButton(text='✅ ℹИнформация', callback_data='info'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ ℹИнформация', callback_data='info'))

        if query.keyboard.tel:
            menu_inlane.insert(InlineKeyboardButton(text='✅ Телефоны', callback_data='tel'))
        else:
            menu_inlane.insert(InlineKeyboardButton(text='❌ Телефоны', callback_data='tel'))

        menu_inlane.insert(InlineKeyboardButton(text='Сохранить', callback_data='exit'))
    except Exception as ex:
        logger.debug(ex)
    finally:
        dbhandle.close()
    return menu_inlane
