import asyncio
import csv
import json
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from all_requests.requests_mediagroup import get_info_only_image
from data.config import path
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from keyboards.default import menu
from keyboards.inline.mesto import hide
from keyboards.inline.stock import choise_num, stocks, choise
from loader import dp, bot
from state.states import Stock


async def start_check_stocks(message, state):
    if message.text == 'В главное меню':
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
        if call.data == 'exit':
            await back(call.message, state)
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
            await back(call.message, state)
        elif call.data == 'zero':
            await matching_stock(call, data['group'], 0, state)
        elif call.data == 'low':
            await matching_stock(call, data['group'], 3, state)
        elif call.data == 'norm':
            await matching_stock(call, data['group'], 10, state)
        else:
            await back(call.message, state)
        await Stock.show_stock.set()


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


# @dp.message_handler(content_types=['text'], state='Stock.order')
# async def stocks_order(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         await bot.send_message(message.from_user.id, 'Введите количество:')


@dp.callback_query_handler(state=Stock.show_stock)
async def answer_call(call: types.CallbackQuery, state: FSMContext):
    """Кол беки с инлайн кнопок и показ  1 картинки в ячейках, проверки товара на представленность"""
    async with state.proxy() as data:
        if call.data == 'exit':
            await call.message.answer('Главное меню. Введите артикул. Пример: 80264335', reply_markup=menu)
            await state.reset_state()
            logger.info('Очистил state')
        elif call.data == 'no':
            await back(call.message, state)
        elif call.data == 'yes':
            try:
                for i in data['products']:
                    await call.message.answer('{} {}'.format(i[0][0], i[0][1]))
                    # await Stock.order.set()
                    # await stocks_order(call.message, state)
            except Exception as ex:
                logger.debug('нет товара{}'.format(ex))
        elif call.data == 'hide':
            async with state.proxy() as data:
                for key in data:
                    if str(key).startswith('photo'):
                        asyncio.create_task(delete_message(data['{}'.format(key)]))
        else:
            logger.info('Пользователь {} запросил картинку на арт.{}'.format(call.from_user.id, call.data))
            if os.path.exists(r"{}/base/json/{}_photo.json".format(path, call.data)):
                logger.info('нашел json и вывел результат')
                with open(r"{}/base/json/{}_photo.json".format(path, call.data), "r", encoding='utf-8') as read_file:
                    data_url = json.load(read_file)
                    photo = await call.message.answer_photo(data_url["url_imgs"][0],
                                                            reply_markup=hide)
            else:
                with open('{}/stikers/seach.tgs'.format(path), 'rb') as sticker:
                    sticker = await call.message.answer_sticker(sticker)
                try:
                    data_url = get_info_only_image(call.data)
                    photo = await call.message.answer_photo(data_url['url_imgs'][0],
                                                            reply_markup=hide)
                except Exception as ex:
                    logger.debug(ex)
                finally:
                    asyncio.create_task(delete_message(sticker))

            try:
                if 'photo{}'.format(call.data) in data:
                    for key in data:
                        if str(key).startswith('photo'):
                            asyncio.create_task(delete_message(data['{}'.format(key)]))

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
                    line.append('{} \nна складе: {}'.format(' '.join(key), dict_art_012[key]))
            if len(line) > 0:
                await bot.send_message(call.from_user.id, '🆘Товары которые необходимо выставить:🆘', reply_markup=menu)
                for item in line:
                    await bot.send_message(call.from_user.id, '{}'.format(item),
                                           reply_markup=InlineKeyboardMarkup().add(
                                               InlineKeyboardButton(text='Показать фото',
                                                                    callback_data='{}'.format(
                                                                        item[:8]
                                                                    ))))
                # await bot.send_message(call.from_user.id, 'Хотите добавить товары в заказ?', reply_markup=choise)
            else:
                await bot.send_message(call.from_user.id, 'Все товары вналичие в зале 👌', reply_markup=menu)
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
        else:
            line = ['нет товара для пополнения']
            await back(call, state)
        logger.info('Список товара товара: {}'.format(line))

