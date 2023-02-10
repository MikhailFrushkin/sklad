from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

import bot
from handlers.users.back import back
from keyboards.default.menu import second_menu
from loader import dp, bot
from state.states import Search
from utils.open_exsel import search_name


async def search(message, state):
    """Выбор склада для поиска артикула"""
    logger.info('Пользователь {}: {} {} запустил поиск на складе'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username
    ))
    mes1 = await bot.send_message(message.from_user.id, 'Введите полностью название или часть:',
                                  reply_markup=second_menu)
    async with state.proxy() as data:
        data['message1'] = mes1

    await Search.search_name.set()


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
