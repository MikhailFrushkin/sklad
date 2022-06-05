import asyncio
import csv

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from data.config import path
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from keyboards.default import menu
from keyboards.inline.stock import choise_num, stocks
from loader import dp, bot
from state.states import Stock


async def start_check_stocks(message, state):
    if message.text == 'Назад':
        await back(message, state)
    mes = await bot.send_message(message.from_user.id, 'Выберите группу товара:', reply_markup=stocks)
    async with state.proxy() as data:
        data['message_temp'] = mes
    await Stock.group.set()


@dp.callback_query_handler(state=Stock.group)
async def check_groups(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = call.data
        asyncio.create_task(delete_message(data['message_temp']))
        match call.data:
            case 'exit':
                await back(call.message, state)
            case _:
                mes = await bot.send_message(call.from_user.id, 'Выберите количество в зале:',
                                             reply_markup=choise_num)
        data['message_temp'] = mes
        await Stock.nums.set()


@dp.callback_query_handler(state=Stock.nums)
async def choise_nums(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        logger.info('Пользователь {} {} запустил проверку на представленность товара, группы {}({})'.format(
            call.from_user.id, call.from_user.first_name, data['group'], call.data
        ))
        asyncio.create_task(delete_message(data['message_temp']))
        match call.data:
            case 'exit':
                await back(call.message, state)
            case 'zero':
                await matching_stock(call, data['group'], 0, state)
            case 'low':
                await matching_stock(call, data['group'], 3, state)
            case 'norm':
                await matching_stock(call, data['group'], 10, state)
            case _:
                await back(call.message, state)
        await Stock.show_stock.set()


def union_art(sklad: str, group: str) -> dict[str, int]:
    with open('{}/utils/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        result = dict()
        for row in reader:
            if row['ТГ'] == group:
                if row['Доступно'].replace('.0', '').isdigit() and not row['Местоположение'].startswith('012_825-OX') \
                        and not row['Местоположение'].startswith('012_825-Dost'):
                    try:
                        result[row['Код \nноменклатуры']] += int(row['Доступно'].replace('.0', ''))
                    except KeyError:
                        result[row['Код \nноменклатуры']] = int(row['Доступно'].replace('.0', ''))
    return result


async def matching_stock(call, group: str, nums: int, state: FSMContext):
    dict_art_012 = union_art('012_825', group)
    dict_art_v = union_art('V_Sales', group)
    line = []
    match nums:
        case 0:
            for key in dict_art_012.keys():
                if key not in dict_art_v.keys():
                    line.append('{} на складе: {}'.format(key, dict_art_012[key]))
            if len(line) > 0:
                await bot.send_message(call.from_user.id, 'Товары которые необходимо выставить:', reply_markup=menu)
                await bot.send_message(call.from_user.id, '{}'.format('\n'.join(line)))
            else:
                await bot.send_message(call.from_user.id, 'Все товары вналичие в зале', reply_markup=menu)
        case 3:
            await bot.send_message(call.from_user.id, 'Товары которые можно пополнить:', reply_markup=menu)
            count = 0
            for key in dict_art_012.keys():
                if key in dict_art_v.keys():
                    if dict_art_v[key] in [1, 2, 3]:
                        count += 1
                        line.append('{} в зале: {} на складе: {}'.format(key, dict_art_v[key], dict_art_012[key]))
                        if count == 20:
                            await bot.send_message(call.from_user.id, '{}'.format('\n'.join(line)))
                            line = []
                            count = 0
        case 10:
            await bot.send_message(call.from_user.id, 'Товары которые можно пополнить:', reply_markup=menu)
            count = 0
            for key in dict_art_012.keys():
                if key in dict_art_v.keys():
                    if dict_art_v[key] in [4, 5, 6, 7, 8, 9, 10]:
                        count += 1
                        line.append('{} в зале: {} на складе: {}'.format(key, dict_art_v[key], dict_art_012[key]))
                        if count == 20:
                            await bot.send_message(call.from_user.id, '{}'.format('\n'.join(line)))
                            line = []
                            count = 0
        case _:
            await back(call, state)
    await state.reset_state()


if __name__ == '__main__':
    matching_stock('11')
