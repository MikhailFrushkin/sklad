import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

import bot
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from keyboards.default.menu import second_menu
from keyboards.inline.mesto import search_sklad_b
from keyboards.inline.quit import exitqr
from loader import dp, bot
from state.states import Search
from utils.open_exsel import search_articul, search_all_sklad, search_art_name, search_name
from utils.read_bd import set_order


async def search(message, state):
    """Выбор склада для поиска артикула"""
    logger.info('Пользователь {}: {} {} запустил поиск на складе'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username
    ))
    mes1 = await bot.send_message(message.from_user.id, '🔍',
                                  reply_markup=second_menu)
    mes2 = await bot.send_message(message.from_user.id, 'Выберите склад:',
                                  reply_markup=search_sklad_b)
    async with state.proxy() as data:
        data['message1'] = mes1
        data['message2'] = mes2

    await Search.sklad.set()


@dp.message_handler(content_types=['text'], state=Search.order)
async def order_num(message: types.Message, state: FSMContext):
    num = message.text
    async with state.proxy() as data:
        if num == 'В главное меню':
            await back(message, state)
        else:
            if not num.isdigit():
                await bot.send_message(message.from_user.id, 'Неверное количество', reply_markup=second_menu)
            else:
                data['order_num'] = num

        logger.info(data['order'])
        logger.info(data['order_num'])
        set_order(message.from_user.id, data['order'], data['order_num'])
    await Search.art.set()
    await bot.send_message(message.from_user.id,
                           '⚠Введите артикул для поиска на {} складе⚠'.format(data['sklad']),
                           reply_markup=exitqr)


@dp.callback_query_handler(state=[Search.sklad, Search.art])
async def input_art(call: types.CallbackQuery, state: FSMContext):
    """
    Поиск по складам введенного артикула
    """
    async with state.proxy() as data:
        if call.data == 'exit':
            await back(call, state)
        elif call.data.startswith('or'):
            await bot.send_message(call.from_user.id, 'Ввeдите количество:', reply_markup=second_menu)
            data['order'] = call.data[2:]
            await Search.order.set()
        elif call.data == 'name':
            await bot.send_message(call.from_user.id, 'Введите название товара:', reply_markup=second_menu)
            await Search.search_name.set()
        else:
            await bot.send_message(call.from_user.id, 'Введите артикул', reply_markup=second_menu)
            await Search.art.set()
            data['sklad'] = call.data
        asyncio.create_task(delete_message(data['message1']))
        asyncio.create_task(delete_message(data['message2']))


@dp.message_handler(content_types=['text'], state=Search.search_name)
async def bot_message2(message: types.Message, state: FSMContext):
    name = message.text.lower()
    logger.info('Пользователь {} {} запустил поиск по названию: {}'.format(message.from_user.id,
                                                                           message.from_user.first_name,
                                                                           name))
    answer = search_name(name)
    logger.info('Получени ответ: {}'.format(answer))
    block_message = []
    if len(answer) > 0:
        count = 0
        for i in answer:
            count += 1
            block_message.append(i)
            if count == 25:
                await bot.send_message(message.from_user.id, '{}'.format('\n'.join(block_message)))
                block_message = []
                count = 0
        await bot.send_message(message.from_user.id, '{}'.format('\n'.join(block_message)))
    else:
        await bot.send_message(message.from_user.id, 'Ни чего не найдено на складе, по запросу: {}'.format(name))
    await back(message, state)


@dp.message_handler(content_types=['text'], state=Search.art)
async def search_sklad(message: types.Message, state: FSMContext):
    """
    Выбор склада
    """
    async with state.proxy() as data:
        if data['sklad'] == 'all':
            if message.text == 'В главное меню':
                await back(message, state)
            else:
                await bot.send_message(message.from_user.id, '{}'.format(search_art_name(message.text)))
                sklad_list = ['011_825', '012_825', 'A11_825', 'V_Sales', 'RDiff']
                for i in sklad_list:
                    cells = search_all_sklad(message.text, i)
                    if cells:
                        logger.info('Вернул список ячеек - {}: {}'.format(message.text, cells))
                        for item in cells:
                        #     if i == '012_825':
                        #         await bot.send_message(message.from_user.id, item,
                        #                                reply_markup=InlineKeyboardMarkup(row_width=1).
                        #                                add(InlineKeyboardButton(text='Заказать',
                        #                                                         callback_data='or{}'.format(
                        #                                                             message.text))))
                        #     else:
                            await bot.send_message(message.from_user.id, item)

                await bot.send_message(message.from_user.id, '⚠Введите артикул для поиска на всех складах⚠',
                                       reply_markup=exitqr)
                await Search.art.set()
        else:
            if message.text == 'В главное меню':
                await back(message, state)
            else:
                cells = search_articul(message.text, data['sklad'])
                if cells:
                    if len(cells) != 0:
                        logger.info('Вернул список ячеек - {}'.format(cells))
                        for item in cells:
                            # if data['sklad'] == '012_825':
                            #     await bot.send_message(message.from_user.id, item,
                            #                            reply_markup=InlineKeyboardMarkup(row_width=1).
                            #                            add(InlineKeyboardButton(text='Заказать',
                            #                                                     callback_data='or{}'.
                            #                                                     format(message.text))))
                            # else:
                            await bot.send_message(message.from_user.id, item)

                await bot.send_message(message.from_user.id,
                                       '⚠Введите артикул для поиска на {} складе⚠'.format(data['sklad']),
                                       reply_markup=exitqr)
                await Search.art.set()
