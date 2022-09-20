import asyncio
import csv
import json
import os
import pandas as pd

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from all_requests.parse_on_requests import parse
from all_requests.requests_mediagroup import get_info
from data.config import path
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from keyboards.default import menu
from keyboards.inline.mesto import hide
from keyboards.inline.stock import choise_num, stocks
from loader import dp, bot
from state.states import Stock
from utils.min_stocks import finish, save_exsel_min, get_groups


async def start_check_stocks(message, state):
    if message.text == 'В главное меню':
        await back(message, state)
    mes = await bot.send_message(message.from_user.id, 'Выберите группу товара:', reply_markup=stocks)
    async with state.proxy() as data:
        data['message_temp'] = mes
    await Stock.group.set()


@dp.callback_query_handler(state=[Stock.group])
async def check_groups(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = call.data
        asyncio.create_task(delete_message(data['message_temp']))
        if call.data == 'exit':
            await back(call, state)
        elif call.data == 'files':
            logger.info('{} {} выгрузил файлы с 0 остатками'.format(call.from_user.id, call.from_user.first_name))
            try:
                groups_list = save_exsel_pst(creat_pst())
                for i in groups_list:
                    try:
                        await call.message.answer_document(open('{}/files/pst_{}.xlsx'.format(path, i), 'rb'))
                    except Exception as ex:
                        logger.debug('Не удалось выгрузить файл {}'.format(ex))
            except Exception as ex:
                logger.info(ex)
            await back(call, state)
        elif call.data == 'min':
            groups = get_groups()
            choise_group = InlineKeyboardMarkup(row_width=3)
            try:
                for i in groups:
                    choise_group.insert(InlineKeyboardButton(text=i[1], callback_data=i[0]))
                choise_group.insert(InlineKeyboardButton(text='Выход', callback_data='exit'))
            except Exception as ex:
                print(ex)
            await Stock.min_vitrina.set()
            await bot.send_message(call.from_user.id, 'Выберите группу:',
                                   reply_markup=choise_group)
        else:
            mes = await bot.send_message(call.from_user.id, 'Количество в зале:',
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
        if call.data == 'exit':
            await back(call, state)
        elif call.data == 'zero':
            await matching_stock(call, data['group'], 0, state)
        elif call.data == 'low':
            await matching_stock(call, data['group'], 3, state)
        elif call.data == 'norm':
            await matching_stock(call, data['group'], 10, state)
        else:
            await back(call, state)
        await Stock.show_stock.set()


@dp.callback_query_handler(state=Stock.show_stock)
async def answer_call(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == 'exit':
            await back(call, state)
        elif call.data == 'no':
            await back(call, state)
        elif call.data == 'yes':
            try:
                for i in data['products']:
                    await call.message.answer('{} {}'.format(i[0][0], i[0][1]))
            except Exception as ex:
                logger.debug('нет товара{}'.format(ex))
        elif call.data == 'hide':
            for key in data:
                if str(key).startswith('photo'):
                    asyncio.create_task(delete_message(data['{}'.format(key)]))
        else:
            logger.info('Пользователь {} запросил картинку на арт.{}'.format(call.from_user.id, call.data))
            data2 = parse(call.data)
            if not data2:
                data2 = get_info(call.data)
            try:
                photo = await call.message.answer_photo(data2['pictures'][0], reply_markup=hide)
            except Exception as ex:
                try:
                    photo = await call.message.answer_photo(data2['pictures'][1], reply_markup=hide)
                    logger.debug(ex)
                except Exception as ex:
                    photo = await call.message.answer_photo('https://jackwharperconstruction.com/wp-content/uploads/9/c/9/9c980deb1f9f42ef2244b13de3aa118d.jpg', reply_markup=hide)
                    logger.debug(ex)
            try:
                data['photo{}'.format(call.data)] = photo
            except Exception as ex:
                logger.debug(ex)


async def matching_stock(call, group: str, nums: int, state: FSMContext):
    async with state.proxy() as data:
        data['products'] = []
        line = []
        if nums == 0:
            dict_art_012 = union_art('012_825', group)[1]
            dict_art_v = union_art('V_Sales', group)[1]
            for key in dict_art_012.keys():
                if key not in dict_art_v.keys():
                    data['products'].append((key, dict_art_012[key]))
                    line.append('{} \nНа складе: {}'.format(' '.join(key), dict_art_012[key]))
            if len(line) > 0:
                await bot.send_message(call.from_user.id, '🆘Товары которые необходимо выставить:🆘', reply_markup=menu)
                for item in line:
                    await bot.send_message(call.from_user.id, '{}'.format(item),
                                           reply_markup=InlineKeyboardMarkup().add(
                                               InlineKeyboardButton(text='Показать фото',
                                                                    callback_data='{}'.format(
                                                                        item[:8]
                                                                    ))))
            else:
                await bot.send_message(call.from_user.id, 'Все товары в наличии👌', reply_markup=menu)
        elif nums == 3:
            dict_art_012 = union_art('012_825', group)[0]
            dict_art_v = union_art('V_Sales', group)[0]
            await bot.send_message(call.from_user.id, '⚠️Товары которые можно пополнить:⚠️', reply_markup=menu)
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
            await bot.send_message(call.from_user.id, '{}'.format('\n'.join(line)))
        elif nums == 10:
            dict_art_012 = union_art('012_825', group)[0]
            dict_art_v = union_art('V_Sales', group)[0]
            await bot.send_message(call.from_user.id, '⚠Товары которые можно пополнить:⚠️', reply_markup=menu)
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
            await bot.send_message(call.from_user.id, '{}'.format('\n'.join(line)))
        else:
            line = ['нет товара для пополнения']
            await back(call, state)


def creat_pst():
    groups_list = ['11', '20', '21', '22', '23', '28', '35']
    mini_group = ['Напольные', 'Костюмные', 'Кресла груши', 'Настенные']
    result_for_zero = dict()
    temp_list = []
    art = []
    groups_second_list = []
    for item in groups_list:
        dict_art_012 = union_art('012_825', item)[1]
        dict_art_v = union_art('V_Sales', item)[1]
        count = 0
        for key in dict_art_012.keys():
            if key not in dict_art_v.keys():
                art.append(key[0])
                count += 1
        if count > 0:
            groups_second_list.append(item)
            with open('{}/utils/file_012_825.csv'.format(path), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['ТГ'] == '35' == item \
                            and row['Краткое наименование'] in mini_group \
                            and row['Код \nноменклатуры'] in art \
                            and row['Доступно'].replace('.0', '').isdigit() \
                            and not row['Местоположение'].startswith('012_825-OX') \
                            and not row['Местоположение'].startswith('012_825-Dost'):
                        temp_list.append([row['Код \nноменклатуры'],
                                          row['Описание товара'].replace(',', ' '),
                                          row['Местоположение'],
                                          row['Доступно'].replace('.0', '')])
                    elif row['ТГ'] == item and row['Код \nноменклатуры'] in art \
                            and row['Доступно'].replace('.0', '').isdigit() \
                            and not row['Местоположение'].startswith('012_825-OX') \
                            and not row['Местоположение'].startswith('012_825-Dost'):
                        temp_list.append([row['Код \nноменклатуры'],
                                          row['Описание товара'].replace(',', ' '),
                                          row['Местоположение'],
                                          row['Доступно'].replace('.0', '')])

                result_for_zero[item] = sorted(temp_list)

                temp_list = []
    return result_for_zero, groups_second_list


def save_exsel_pst(data):
    groups_list = data[1]
    for item in groups_list:
        with open('{}/files/result_{}.csv'.format(path, item), 'w', encoding='utf-8') as file:
            file.write("Код номенклатуры,"
                       "Описание товара,"
                       "Местоположение,"
                       "Доступно\n")
            for i in data[0][item]:
                file.write('{}\n'.format(','.join(i)))
        try:
            df = pd.read_csv('{}/files/result_{}.csv'.format(path, item), encoding='utf-8')
            writer = pd.ExcelWriter('{}/files/pst_{}.xlsx'.format(path, item))
            df.style.apply(align_left, axis=0).to_excel(writer, sheet_name='Sheet1', index=False, na_rep='NaN')
            writer.sheets['Sheet1'].set_column(0, 4, 20)
            writer.sheets['Sheet1'].set_column(1, 1, 50)
            writer.save()
        except Exception as ex:
            logger.debug(ex)
    return groups_list


def union_art(sklad: str, group: str):
    with open('{}/utils/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        result_for_zero = dict()
        result = dict()
        mini_group = ['Напольные', 'Костюмные', 'Кресла груши', 'Настенные']
        for row in reader:
            if group == '35':
                if row['ТГ'] == '35' and row['Краткое наименование'] in mini_group:
                    if row['Доступно'].replace('.0', '').isdigit() and not row['Местоположение'].startswith(
                            '012_825-OX') \
                            and not row['Местоположение'].startswith('012_825-Dost'):
                        result = _union_result(row, result)
                        result_for_zero = _union_result_for_zero(row, result_for_zero)
            elif group == '23':
                if row['ТГ'] in ['23', '27']:
                    if row['Доступно'].replace('.0', '').isdigit() and not row['Местоположение'].startswith(
                            '012_825-OX') \
                            and not row['Местоположение'].startswith('012_825-Dost'):
                        result = _union_result(row, result)
                        result_for_zero = _union_result_for_zero(row, result_for_zero)
            elif group == '28':
                if row['ТГ'] in ['24', '28']:
                    if row['Доступно'].replace('.0', '').isdigit() and not row['Местоположение'].startswith(
                            '012_825-OX') \
                            and not row['Местоположение'].startswith('012_825-Dost'):
                        result = _union_result(row, result)
                        result_for_zero = _union_result_for_zero(row, result_for_zero)
            else:
                if row['ТГ'] == group:
                    if row['Доступно'].replace('.0', '').isdigit() and not row['Местоположение'].startswith(
                            '012_825-OX') \
                            and not row['Местоположение'].startswith('012_825-Dost'):
                        result = _union_result(row, result)
                        result_for_zero = _union_result_for_zero(row, result_for_zero)
    return result, result_for_zero


def _union_result(row: dict, result: dict) -> dict:
    try:
        result[row['Код \nноменклатуры']] += int(row['Доступно'].
                                                 replace('.0', ''))
    except KeyError:
        result[row['Код \nноменклатуры']] = int(row['Доступно'].
                                                replace('.0', ''))
    return result


def _union_result_for_zero(row: dict, result_for_zero) -> dict:
    try:
        result_for_zero[(row['Код \nноменклатуры'], row['Описание товара'])] += int(row['Доступно'].
                                                                                    replace('.0', ''))
    except KeyError:
        result_for_zero[(row['Код \nноменклатуры'], row['Описание товара'])] = int(row['Доступно'].
                                                                                   replace('.0', ''))
    return result_for_zero


def align_left(x):
    return ['text-align: left' for x in x]


@dp.callback_query_handler(state=Stock.min_vitrina)
async def min_vitrina(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'exit':
        await back(call, state)
    else:
        result = finish(call.data)[0]
        count = 0
        line = []
        try:
            for i in result:
                count += 1
                line.append(i)
                if count == 20:
                    await bot.send_message(call.from_user.id, '\n'.join(line))
                    count = 0
                    line = []
            if len(line) > 0:
                await bot.send_message(call.from_user.id, '\n'.join(line))
        except Exception:
            logger.debug('Нет товара для вывода мин.витрины')
        save_exsel_min(call.data)
        try:
            logger.info('{} {} запросил мин.витрину на {}'.format(call.from_user.id,
                                                                  call.from_user.first_name,
                                                                  call.data))
            await call.message.answer_document(open('{}/files/min_vitrina_{}.xlsx'.format(path, call.data), 'rb'))
        except Exception as ex:
            logger.debug('Не удалось выгрузить файл для {} {}'.format(call.data, ex))
            await bot.send_message(call.from_user.id, 'Все товары в достаточном количестве.')
        await back(call, state)


if __name__ == '__main__':
    save_exsel_pst(creat_pst())
