import asyncio
import csv
import os

import pandas as pd
from data.config import ADMINS

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from all_requests.parse_on_requests import parse
from all_requests.requests_mediagroup import get_info
from data.config import path
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from keyboards.default.menu import menu, menu_admin
from keyboards.inline.graf import graf_days
from keyboards.inline.mesto import hide
from keyboards.inline.stock import choise_num, stocks
from loader import dp, bot
from state.states import Stock, Graf
from utils.min_stocks import finish, save_exsel_min, get_groups


@dp.callback_query_handler(state=[Graf.check_graf])
async def check_graf(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'exit':
        await back(call, state)
    elif call.data == 'days':
        await bot.send_message(call.from_user.id, 'Выберите день', reply_markup=graf_days)
        await Graf.day_graf.set()


@dp.callback_query_handler(state=[Graf.day_graf])
async def check_graf(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'exit':
        await back(call, state)
    else:
        day = call.data
        try:
            excel_data_df = pd.read_excel('{}/График.xls'.format(path))
            excel_data_df.to_csv('{}/График.scv'.format(path))
            line = []
            with open('{}/График.scv'.format(path), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row[day][:2].isdigit():
                        line.append('{}\n{} по {}'.format(row['ФИО'],
                                                          'Дежурный c ' + row[day][:5] if row[day][:5].startswith(
                                                              '09:00') else 'c ' + row[day][:5], row[day][6:]))
                await bot.send_message(call.from_user.id, '\n'.join(line))
                await back(call, state)
        except Exception as ex:
            logger.debug(ex)
        finally:
            os.remove('{}/График.scv'.format(path))
