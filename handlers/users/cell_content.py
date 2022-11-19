import asyncio
import json
import os
import os.path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

import bot
from all_requests.parse_on_requests import parse
from data.config import path
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from handlers.users.helps import bot_help
from keyboards.default.menu import second_menu
from keyboards.inline.mesto import mesto1
from keyboards.inline.mesto import mesto2, mesto3, hide
from loader import bot
from loader import dp
from state.states import Place
from state.states import Search
from utils.open_exsel import place, place_dost


async def show_place(message, state):
    """Просмотр содержимого ячейки"""
    ans = message.text
    if ans == 'В главное меню':
        await back(message, state)
    elif ans == 'Помощь':
        await bot_help(message)
    else:
        logger.info('Пользователь {}: {} {} запустил просмотр ячеек'.format(
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.username
        ))
        await Place.mesto_1.set()
        async with state.proxy() as data:
            data['command'] = message.get_command()
            data['message_id'] = message.message_id
            await bot.send_message(message.from_user.id, '📦 \n',
                                   reply_markup=second_menu)
            mes1 = await bot.send_message(message.from_user.id, 'Выберите ряд:',
                                          reply_markup=mesto1)
            data['message1'] = mes1


@dp.callback_query_handler(state=Place.mesto_1)
async def place_1(call: types.CallbackQuery, state: FSMContext):
    """Поиск по рядам"""
    async with state.proxy() as data:
        if call.data == '012_825-OX':
            data['mesto1'] = call.data
            asyncio.create_task(delete_message(data['message1']))
            mes = place('012_825-OX', '012_825')
            if mes == 'Ячейка пуста':
                await call.message.answer('{}'.format(mes))
            else:
                await call.message.answer('\n'.join(mes))
            await back(call, state)
        elif call.data == 'dost':
            data['mesto1'] = call.data
            asyncio.create_task(delete_message(data['message1']))
            dost_list = place_dost('012_825-Dost', '012_825')
            logger.info(dost_list)
            count = 0
            list_1 = []
            if dost_list:
                if dost_list != 'В ячейках нет отказанного товара':
                    for item in range(len(dost_list)):
                        list_1.append(dost_list[item])
                        count += 1
                        if count == 20:
                            await call.message.answer('\n'.join(list_1))
                            list_1 = []
                            count = 0
                    await call.message.answer('\n'.join(list_1))
                else:
                    await bot.send_message(call.from_user.id, 'В ячейках нет отказаного товара.')
            await back(call, state)
        elif call.data == 'rdiff':
            data['mesto1'] = call.data
            asyncio.create_task(delete_message(data['message1']))
            rdiff_list = place('RDiff_825-1', 'RDiff')
            count = 0
            list_1 = []
            for item in range(len(rdiff_list)):
                list_1.append(rdiff_list[item])
                count += 1
                if count == 20:
                    await call.message.answer('\n'.join(list_1))
                    list_1 = []
                    count = 0
            await call.message.answer('\n'.join(list_1))
            await back(call, state)
        else:
            answer_p = call.data
            asyncio.create_task(delete_message(data['message1']))
            mes1 = await call.message.answer('Выберите секцию:', reply_markup=mesto2)
            data['mesto1'] = answer_p
            data['message1'] = mes1
            await Place.mesto_2.set()


@dp.callback_query_handler(state=Place.mesto_2)
async def place_2(call: types.CallbackQuery, state: FSMContext):
    """Ввод секций для поиска"""
    await call.answer(cache_time=5)
    answer: str = call.data

    async with state.proxy() as data:
        asyncio.create_task(delete_message(data['message1']))
        mes1 = await call.message.answer('Выберите ячейку:', reply_markup=mesto3)
        data['mesto2'] = answer
        data['message1'] = mes1

    await Place.mesto_3.set()


@dp.callback_query_handler(state=Place.mesto_3)
async def place_3(call: types.CallbackQuery, state: FSMContext):
    """Ввод ячейки поиска"""
    await call.answer(cache_time=5)
    answer = call.data
    async with state.proxy() as data:
        data['mesto3'] = answer
        asyncio.create_task(delete_message(data['message1']))
        if len(data['mesto1']) == 1:
            data['mesto1'] = '0{}'.format(data['mesto1'])

        result = '012_825-{}-0{}-{}'.format(
            data['mesto1'],
            data['mesto2'],
            data['mesto3']
        )
        data['result'] = result
        logger.info(data['result'])
        place_list = place(result, '012_825')
        if len(place_list) != 0:
            for item in place_list:
                await call.message.answer(item,
                                          reply_markup=InlineKeyboardMarkup().add(
                                              InlineKeyboardButton(text='Показать фото',
                                                                   callback_data='{}'.format(
                                                                       item[:8]
                                                                   ))))

            await Place.mesto_4.set()
        else:
            await bot.send_message(call.from_user.id, 'Ячейка пустая', reply_markup=second_menu)

            mes1 = await bot.send_message(call.from_user.id, 'Выберите ряд:', reply_markup=mesto1)
            data['message1'] = mes1

            await Place.mesto_1.set()


@dp.callback_query_handler(state=[Place.mesto_4, Search.show_all])
async def answer_call(call: types.CallbackQuery, state: FSMContext):
    """Кол беки с инлайн кнопок и показ  1 картинки в ячейках"""
    async with state.proxy() as data:
        if call.data == 'exit':
            await back(call, state)
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
                if os.path.exists(r"{}\base\json\{}.json".format(path, call.data)):
                    logger.info('нашел json ')
                    with open(r"{}\base\json\{}.json".format(path, call.data), 'r', encoding='utf-8') as file:
                        data2 = json.load(file)
                    photo = await call.message.answer_photo(data2['pictures'][0], reply_markup=hide)
                    logger.debug(ex)
            data['photo{}'.format(call.data)] = photo
