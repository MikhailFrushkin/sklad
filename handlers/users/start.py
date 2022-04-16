import asyncio
import json
import os.path
from contextlib import suppress

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from loguru import logger

import bot
from keyboards.default import menu
from keyboards.inline.mesto import mesto1, mesto2, mesto3, hide
from keyboards.inline.quit import exitqr
from loader import dp, bot
from requests_mediagroup import get_info
from show_tabel import get_graf
from state.show_photo import Showphoto, Place
from utils.new_qr import qr_code
from utils.open_exsel import place


async def delete_message(message: types.Message, sleep_time: int = 0):
    """Удаление сообщений, в данном случае стикера ожидания"""
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """
    Старт бота
    """
    sticker = open('stikers/AnimatedSticker2.tgs', 'rb')
    await bot.send_sticker(message.chat.id, sticker)
    await message.answer('Добро пожаловать, {}!'
                         '\nДля показа фотографий товара, описания и цены с сайта'
                         '\nВведите артикул. Пример: 80264335.'
                         '\nДля показа Qrcode ячейки на складе нажмите на '
                         '"Показать qrcode ячейки" или воспользуйтесь кнопками.'
                         '\nДля показа товара на ячейках нажмите "Содержимое ячейки".'
                         .format(message.from_user.first_name), reply_markup=menu)


@dp.message_handler(commands=['showqr'], state='*')
async def show_qr(message: types.Message, state: FSMContext):
    """
    Тригер на команду showqr и отправляет с кнопки.
    """
    logger.info('Пользователь {}: {} {} запросил команду /showqr'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username
    ))

    await bot.send_message(message.from_user.id, 'Для показа Qrcode введите ряд, секцию, ячейку без нулей и пробела')
    async with state.proxy() as data:
        data['command'] = message.get_command()
        data['message_id'] = message.message_id

    await Showphoto.show_qr.set()


@dp.message_handler(commands=['graph'], state='*')
async def show_graf(message: types.Message, state: FSMContext):
    """
    Тригер на команду showqr и отправляет с кнопки.
    """
    logger.info('Пользователь {}: {} {} запросил команду /Мой график'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username
    ))

    await bot.send_message(message.from_user.id, 'График на текущий месяц')
    try:
        with open('stikers/seach.tgs', 'rb') as sticker:
            sticker = await bot.send_sticker(message.chat.id, sticker)
        get_graf(message)
        graf = open('base/graf/{}.png'.format(message.from_user.id), 'rb')
        await bot.send_photo(message.chat.id, graf)
        asyncio.create_task(delete_message(sticker))
    except Exception as ex:
        logger.debug(ex)

    async with state.proxy() as data:
        data['command'] = message.get_command()
        data['message_id'] = message.message_id

    await state.reset_state()
    logger.info('Очистил state')


@dp.message_handler(state=Showphoto.show_qr)
async def showqr(message: types.Message, state: FSMContext):
    """
    Функция отправки qcodes.
    Ели сообщение удовлетворяет условию, генерирует код и отправляет.
    Скидывает стате.
    """
    ans = message.text
    if ans.isdigit():
        if len(ans) == 3:
            if 0 < int(ans[1]) < 9 and int(ans[2]) < 5:

                await bot.send_message(message.from_user.id, '{} ряд {} секция {} ячейка'.
                                       format(ans[0], ans[1], ans[2]))

                data = ('012_825-0{}-0{}-{}'.format(message.text[0], message.text[1], message.text[2]))
                qr_code(message, data)
                qrcod = open('qcodes/{}.jpg'.format(message.text), 'rb')
                await bot.send_photo(message.from_user.id, qrcod)

                await state.reset_state()
                logger.info('Очистил state')
            else:
                await bot.send_message(message.from_user.id,
                                       'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела',
                                       reply_markup=exitqr)
        elif len(ans) == 4 and int(ans[0]) == 1 and 0 < int(ans[1]) < 8:
            if 0 < int(ans[2]) < 9 and int(ans[3]) < 5:

                await bot.send_message(message.from_user.id, '{}{} ряд {} секция {} ячейка'.
                                       format(ans[0], ans[1], ans[2], ans[3]))

                data = ('012_825-{}{}-0{}-{}'
                        .format(message.text[0], message.text[1], message.text[2], message.text[3]))

                qr_code(message, data)
                qrcod = open('qcodes/{}.jpg'.format(message.text), 'rb')
                await bot.send_photo(message.from_user.id, qrcod)

                await state.reset_state()
                logger.info('Очистил state')
            else:
                await bot.send_message(message.from_user.id,
                                       'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела',
                                       reply_markup=exitqr)
        else:
            await bot.send_message(message.from_user.id,
                                   'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела',
                                   reply_markup=exitqr)
    else:
        await bot.send_message(message.from_user.id, 'Введены буквы или символы',
                               reply_markup=exitqr)


@dp.callback_query_handler(state=[Showphoto.show_qr, Place.mesto_4])
async def answer_exit(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'exit':
        await call.answer(cache_time=10)
        answer: str = call.data
        logger.info('Получил ответ: {}. Сохраняю в state'.format(answer))
        await call.message.answer('Введите артикул. Пример: 80264335')
        await state.reset_state()
        logger.info('Очистил state')
    elif call.data == 'hide':
        async with state.proxy() as data:
            asyncio.create_task(delete_message(data['photo']))
    else:
        logger.info('Пользователь запросил картинку на арт.{}'.format(call.data))
        if os.path.exists('base/{}.json'.format(call.data)):
            logger.info('нашел json и вывел результат')
            with open('base/{}.json'.format(call.data), "r", encoding='utf-8') as read_file:
                data = json.load(read_file)
                media = types.MediaGroup()
                photo = await call.message.answer_photo(data["url_imgs"][0],
                                                        reply_markup=hide)
        else:
            with open('stikers/seach.tgs', 'rb') as sticker:
                sticker = await call.message.answer_sticker(sticker)
            url = get_info(call.data)
            photo = await call.message.answer_photo(url[0][0],
                                                    reply_markup=hide)
            asyncio.create_task(delete_message(sticker))
        async with state.proxy() as data:
            data['photo'] = photo


async def show_place(message, state):
    logger.info('Пользователь {}: {} {} запустил просмотр ячеек'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username
    ))

    mes1 = await bot.send_message(message.from_user.id, 'Данные на 15.04.22\nВыберите ряд:', reply_markup=mesto1)
    async with state.proxy() as data:
        data['command'] = message.get_command()
        data['message_id'] = message.message_id
        data['message1'] = mes1

    await Place.mesto_1.set()


@dp.callback_query_handler(state=Place.mesto_1)
async def place_1(call: types.CallbackQuery, state: FSMContext):
    if call.data == '012_825-OX':
        async with state.proxy() as data:
            data['mesto1'] = call.data
            asyncio.create_task(delete_message(data['message1']))
            await call.message.answer('\n'.join(place('012_825-OX')))
            await state.reset_state()
            logger.info('Очистил state')
    else:
        await call.answer(cache_time=10)
        answer: str = call.data
        logger.info('Получил ряд: {}'.format(answer))
        mes2 = await call.message.answer('Выберите секцию:', reply_markup=mesto2)
        async with state.proxy() as data:
            data['mesto1'] = answer
            data['message2'] = mes2
            asyncio.create_task(delete_message(data['message1']))
        await Place.mesto_2.set()


@dp.callback_query_handler(state=Place.mesto_2)
async def place_2(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=10)
    answer: str = call.data
    logger.info('Получил секцию: {}'.format(answer))
    mes3 = await call.message.answer('Выберите ячейку:', reply_markup=mesto3)
    async with state.proxy() as data:
        data['mesto2'] = answer
        data['message3'] = mes3
        asyncio.create_task(delete_message(data['message2']))
    await Place.mesto_3.set()


@dp.callback_query_handler(state=Place.mesto_3)
async def place_3(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=10)
    answer: str = call.data
    logger.info('Получил ячейку: {}. '.format(answer))

    async with state.proxy() as data:
        data['mesto3'] = answer
        asyncio.create_task(delete_message(data['message3']))
        if len(data['mesto1']) == 1:
            data['mesto1'] = '0{}'.format(data['mesto1'])

        result = '012_825-{}-0{}-{}'.format(
            data['mesto1'],
            data['mesto2'],
            data['mesto3']
        )
        await call.message.answer('Список товара на {}:'.format(result))
        data['result'] = result
        logger.info(data['result'])

        for item in place(result):
            await call.message.answer(item,
                                      reply_markup=InlineKeyboardMarkup().add(
                                          InlineKeyboardButton(text='Показать фото',
                                                               callback_data='{}'.format(
                                                                   item[:8]
                                                               ))))

        await Place.mesto_4.set()


@dp.message_handler(content_types=['text'], state='*')
async def bot_message(message: types.Message, state: FSMContext):
    """
    Выводим сохраненные qcode ячеек, стандартные.
    Основное, парсим через функцию requests_mediagroup, если уже есть json просто выводим инфу,
    иначе идем циклом по кортежу и выводим инф
    """
    if message.text == '🆚 V-Sales_825':
        await bot.send_message(message.from_user.id, 'V-Sales_825')

        qrc = open('qcodes/V-Sales_825.jpg', 'rb')
        await bot.send_photo(message.chat.id, qrc)

    elif message.text == '☣ R12_BrakIn_825':
        await bot.send_message(message.from_user.id, 'R12_BrakIn_825')

        qrc = open('qcodes/R12_BrakIn_825.jpg', 'rb')
        await bot.send_photo(message.chat.id, qrc)

    elif message.text == '🤖 Показать Qrcode ячейки':
        await show_qr(message, state)

    elif message.text == 'Мой график(в разработке)':
        await show_graf(message, state)

    elif message.text == '📦 Содержимое ячейки':
        await show_place(message, state)

    elif message.text == 'ℹ Информация':
        await bot.send_message(message.from_user.id,
                               'По всем вопросам обращаться к Михаилу, БЮ 825(склад), почта - muxazila@mail.ru')
    else:
        answer = message.text.lower()
        logger.info('Пользователь {} {}: запросил артикул {}'.format(
            message.from_user.id,
            message.from_user.first_name,
            answer
        ))

        if len(answer) == 8 and answer.isdigit() and answer[:2] == '80':
            await show_media(message, state)
        else:
            await bot.send_message(message.from_user.id,
                                   'Неверно указан артикул или его нет на сайте. Пример: 80422781')


async def show_media(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if os.path.exists('base/{}.json'.format(answer)):
        logger.info('нашел json и вывел результат')
        with open('base/{}.json'.format(answer), "r", encoding='utf-8') as read_file:
            data = json.load(read_file)
            await bot.send_message(message.from_user.id, data['name'].replace('#', 'Артикул: '))
            if len(data['url_imgs']) >= 2:
                media = types.MediaGroup()
                if len(data['url_imgs']) < 10:
                    for i_photo in data['url_imgs']:
                        media.attach_photo(i_photo)
                    await message.answer_media_group(media)
                else:
                    for i_photo in range(10):
                        media.attach_photo(data['url_imgs'][i_photo])
                    await message.answer_media_group(media)
            else:
                await message.answer_photo(data['url_imgs'])
            await bot.send_message(message.from_user.id, '\n'.join(data['params']))
            await bot.send_message(message.from_user.id,
                                   'Цена с сайта: {}(Уточняйте в Вашем магазине)'.format(data['price']))
            await state.reset_state()
            logger.info('Очистил state')

    else:
        try:
            with open('stikers/seach.tgs', 'rb') as sticker:
                sticker = await bot.send_sticker(message.chat.id, sticker)

            url_list = get_info(answer)
            await bot.send_message(message.from_user.id, url_list[1].replace('#', 'Артикул: '))
            logger.info('Функция вернула список урл - {}\n'.format(url_list))
            if len(url_list[0]) >= 2:
                media = types.MediaGroup()
                if len(url_list[0]) < 10:
                    for i_photo in url_list[0]:
                        media.attach_photo(i_photo)
                    await message.answer_media_group(media)
                else:
                    for i_photo in range(10):
                        media.attach_photo(url_list[0][i_photo])
                    await message.answer_media_group(media)
            else:
                await message.answer_photo(url_list[0][0])
            await bot.send_message(message.from_user.id, '\n'.join(url_list[2]))
            await bot.send_message(message.from_user.id,
                                   'Цена с сайта: {}(Уточняйте в Вашем магазине)'.format(url_list[3]))
            asyncio.create_task(delete_message(sticker))

        except Exception as ex:
            await bot.send_message(message.from_user.id,
                                   'Неверно указан артикул или его нет на сайте. Пример: 80422781')
            asyncio.create_task(delete_message(sticker))

            logger.debug('{}'.format(ex))
