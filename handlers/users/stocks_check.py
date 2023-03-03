import asyncio
import csv
import pandas as pd
from data.config import ADMINS

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from all_requests.parse_on_requests import parse
from data.config import path
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from handlers.users.edit_keyboard import create_keyboard
from keyboards.default.menu import menu, menu_admin
from keyboards.inline.mesto import hide
from keyboards.inline.stock import choise_num, stocks
from loader import dp, bot
from state.states import Stock
from utils.min_stocks import finish, save_exsel_min, get_groups


async def start_check_stocks(message, state):
    async with state.proxy() as data:
        if message.text == 'В главное меню':
            await back(message, state)
        mes = await bot.send_message(message.from_user.id, 'Выберите группу товара:', reply_markup=stocks)
        data['message_temp'] = mes
        await Stock.group.set()


@dp.callback_query_handler(state=[Stock.group])
async def check_groups(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = call.data
        try:
            asyncio.create_task(delete_message(data['message_temp']))
        except Exception as ex:
            logger.debug(ex)
        if call.data == 'exit':
            await back(call, state)
        elif call.data == 'files':
            logger.info('{} {} выгрузил файлы с 0 остатками'.format(call.from_user.id, call.from_user.first_name))
            try:
                for i in ['11', '20', '21', '22', '23', '28', '35']:
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
                logger.debug(ex)
            await Stock.min_vitrina.set()
            await bot.send_message(call.from_user.id, 'Выберите группу:',
                                   reply_markup=choise_group)
        elif call.data == 'ebel':
            try:
                await call.message.answer_document(open('{}/files/result_ebel.xlsx'.format(path), 'rb'))
            except Exception as ex:
                logger.debug('Не удалось выгрузить файл {}'.format(ex))
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
            try:
                photo = await call.message.answer_photo(data2['pictures'][0], reply_markup=hide)
            except Exception as ex:
                try:
                    photo = await call.message.answer_photo(data2['pictures'][1], reply_markup=hide)
                    logger.debug(ex)
                except Exception as ex:
                    photo = await call.message.answer_photo(
                        'https://jackwharperconstruction.com/wp-content/uploads'
                        '/9/c/9/9c980deb1f9f42ef2244b13de3aa118d.jpg',
                        reply_markup=hide)
                    logger.debug(ex)
            try:
                data['photo{}'.format(call.data)] = photo
            except Exception as ex:
                logger.debug(ex)


async def matching_stock(call, group: str, nums: int, state: FSMContext):
    async with state.proxy() as data:
        data['products'] = []
        line = []
        if call.from_user.id not in [int(i) for i in ADMINS]:
            try:
                menu_check = create_keyboard(call.from_user.id)
            except Exception as ex:
                menu_check = menu
                logger.debug(call.from_user.first_name, ex)
        else:
            menu_check = menu_admin

        if nums == 0:
            dict_art_012 = union_art('012_825', group)[1]
            dict_art_v = union_art('V_Sales', group)[1]
            dict_art_s = union_art('S_825', group)[1]
            for key in dict_art_012.keys():
                if key not in dict_art_v.keys() and key not in dict_art_s.keys():
                    data['products'].append((key, dict_art_012[key]))
                    line.append('{} \nНа складе: {}'.format(' '.join(key), dict_art_012[key]))
            if len(line) > 0:
                await bot.send_message(call.from_user.id, '🆘Товары которые необходимо выставить:🆘',
                                       reply_markup=menu_check)
                for item in line:
                    await bot.send_message(call.from_user.id, '{}'.format(item),
                                           reply_markup=InlineKeyboardMarkup().add(
                                               InlineKeyboardButton(text='Показать фото',
                                                                    callback_data='{}'.format(
                                                                        item[:8]
                                                                    ))))
            else:
                await bot.send_message(call.from_user.id, 'Все товары в наличии👌', reply_markup=menu_check)
        elif nums == 3:
            dict_art_012 = union_art('012_825', group)[0]
            dict_art_v = union_art('V_Sales', group)[0]
            await bot.send_message(call.from_user.id, '⚠️Товары которые можно пополнить:⚠️', reply_markup=menu_check)
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
            await bot.send_message(call.from_user.id, '⚠Товары которые можно пополнить:⚠️', reply_markup=menu_check)
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
    groups_list = ['11', '20', '21', '22', '23', '28', '31', '33', '34', '35', '36', '37', '38', '39', '40', '46', '49']
    mini_group = ['Напольные', 'Костюмные', 'Кресла груши', 'Настенные']
    result_for_zero = dict()
    zero_data = {
        '11': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
        '28': 0,
        '35': 0
    }
    temp_list = []
    temp_list_ebel = []
    art = []
    art_ebel = []
    groups_second_list = []
    for item in groups_list:
        dict_art_012 = union_art('012_825', item)[1]
        dict_art_v = union_art('V_Sales', item)[1]
        dict_art_a11 = union_art('A11_825', item)[1]
        count = 0
        for key in dict_art_012.keys():
            if key not in dict_art_v.keys():
                art.append(key[0])
                count += 1
        for key in dict_art_012.keys():
            if key not in dict_art_v.keys() and key not in dict_art_a11.keys():
                art_ebel.append(key[0])
        if count > 0:
            groups_second_list.append(item)
            with open('{}/files/file_012_825.csv'.format(path), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['ТГ'] == '35' \
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
                    elif row['ТГ'] in ['31', '33', '34', '35', '36', '37', '38', '39', '40', '46', '49'] \
                            and row['Код \nноменклатуры'] in art_ebel \
                            and row['Доступно'].replace('.0', '').isdigit() \
                            and not row['Местоположение'].startswith('012_825-OX') \
                            and not row['Местоположение'].startswith('012_825-Dost'):
                        temp_list_ebel.append([row['Код \nноменклатуры'],
                                               row['Описание товара'].replace(',', ' '),
                                               row['Местоположение'],
                                               row['Доступно'].replace('.0', '')])

                temp_list2 = list(set([i[0] for i in temp_list]))
                zero_data[item] = len(temp_list2)
                result_for_zero[item] = sorted(temp_list)
                temp_list = []
    nulls_ebel = []
    for i in temp_list_ebel:
        if i not in nulls_ebel:
            nulls_ebel.append(i)

    result_for_zero['ebel'] = nulls_ebel

    return result_for_zero, groups_second_list, zero_data


def save_exsel_pst(data):
    groups_list = data[1]
    groups_list2 = ['11', '20', '21', '22', '23', '28', '35']
    for item in groups_list:
        if item in groups_list2:
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
                df.reset_index(drop=True).style.apply(align_left, axis=0). \
                    to_excel(writer, sheet_name='Sheet1', index=False, na_rep='NaN')
                writer.sheets['Sheet1'].set_column(0, 4, 20)
                writer.sheets['Sheet1'].set_column(1, 1, 50)
                writer.close()
            except Exception as ex:
                logger.debug(ex)
    with open('{}/files/result_ebel.csv'.format(path), 'w', encoding='utf-8') as file:
        file.write("Код номенклатуры,"
                   "Описание товара,"
                   "Местоположение,"
                   "Доступно\n")
        for i in data[0]['ebel']:
            file.write('{}\n'.format(','.join(i)))
    try:
        df = pd.read_csv('{}/files/result_ebel.csv'.format(path), encoding='utf-8')
        writer = pd.ExcelWriter('{}/files/result_ebel.xlsx'.format(path))
        df.sort_values('Код номенклатуры').reset_index(drop=True).style.apply(align_left, axis=0). \
            to_excel(writer, sheet_name='Sheet1', index=False, na_rep='NaN')
        writer.sheets['Sheet1'].set_column(0, 4, 20)
        writer.sheets['Sheet1'].set_column(1, 1, 50)
        writer.close()
    except Exception as ex:
        logger.debug(ex)
    return groups_list, data[2]


def union_art(sklad: str, group: str):
    with open('{}/files/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
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
                if row['ТГ'] in ['12', '23', '27'] and row['НГ'] not in ['112', '175', '176', '177']:
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
