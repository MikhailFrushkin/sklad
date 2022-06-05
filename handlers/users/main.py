import asyncio
import datetime
import json
import os
import os.path
import sqlite3
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes
from loguru import logger

import bot
from all_requests.requests_mediagroup import get_info
from data.config import ADMINS, PASSWORD, path
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from handlers.users.helps import bot_help
from handlers.users.search import search
from handlers.users.show_media import show_media
from handlers.users.show_place import show_place
from handlers.users.show_qrs import show_qr
from keyboards.default import menu
from keyboards.default.menu import second_menu, menu_admin, dowload_menu, orders
from keyboards.inline.mesto import mesto2, mesto3, hide, mesto1
from loader import dp, bot
from state.states import Place, Search, Logging, Messages, QR, Orders
from utils.check_bd import check
from utils.open_exsel import place, search_articul, dowload, search_all_sklad, search_art_name, place_dost
from utils.read_bd import set_order, del_orders, mail


@dp.message_handler(commands=['start'], state='*')
async def bot_start(message: types.Message):
    """
    Старт бота, проверка на присутствие в базе данных, если нет, запрашивает пароль
    """
    logger.info('Пользователь {}: {} {} нажал на кнопку {}'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username,
        message.text
    ))
    if check(message.from_user.id):
        sticker = open('{}/stikers/Dicaprio.tgs'.format(path), 'rb')
        await bot.send_sticker(message.chat.id, sticker)
        if str(message.from_user.id) in ADMINS:
            await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре',
                                 reply_markup=menu_admin)
        else:
            await message.answer('Добро пожаловать, {}!'
                                 '\nДля показа фотографий товара, описания и цены с сайта'
                                 '\nВведите артикул. Пример: 80264335.'
                                 '\n"🤖 Показать Qrcode ячейки" - '
                                 '\nДля показа Qrcode ячейки на складе. '
                                 '\n"📦 Содержимое ячейки" - '
                                 '\nДля показа товара на ячейке.'
                                 '\n"🔍 Поиск на складах" - '
                                 '\nДля поиска ячеек, румов и тд. с определенным артикулом.'
                                 .format(message.from_user.first_name), reply_markup=menu)
    else:
        await helps(message)
        await bot.send_message(message.from_user.id, 'Нет доступа, введите пароль!')
        await Logging.log.set()


@dp.message_handler(commands=['help'], state='*')
async def helps(message: types.Message):
    """
    Справка бота
    """
    await bot_help(message)


@dp.message_handler(content_types=['text'], state=Logging.log)
async def bot_message(message: types.Message, state: FSMContext):
    """
    Если пароль верен, вносит в базу пользователя, перезапускает функуию старт"""
    if message.text == PASSWORD:
        connect = sqlite3.connect('{}/base/BD/users.bd'.format(path))
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(id INTEGER, name TEXT, date REAL, БЮ INTEGER)""")
        connect.commit()

        cursor.execute('SELECT id FROM login_id WHERE id = {}'.format(message.from_user.id))
        data = cursor.fetchone()
        if data is None:
            date = datetime.datetime.now()
            shop = 0
            user_id = [message.from_user.id, message.from_user.first_name, date, shop]
            cursor.execute('INSERT INTO login_id VALUES(?,?,?,?);', user_id)
            connect.commit()
        await state.reset_state()
        logger.info('Очистил state')
        await bot_start(message)


@dp.message_handler(content_types=['text'], state=Messages.mes)
async def bot_message(message: types.Message, state: FSMContext):
    """
    Рассылка сообщения пользователям бота,
    нажатие админ кнопки на "отправить"
    """

    if message.text == 'Назад':
        await back(message, state)
    else:
        text_mes = '❗❗❗{}❗❗❗\n'.format(message.text)
        logger.info('Запустил рассылку - {}  от пользователя {}'.format(text_mes, message.from_user.id))

        connect = sqlite3.connect('{}/base/BD/users.bd'.format(path))
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM login_id;")
        one_result = cursor.fetchall()
        for i in one_result:
            await bot.send_message(i[0], text_mes)


@dp.message_handler(content_types=['text'], state=Search.art)
async def search_sklad(message: types.Message, state: FSMContext):
    """
    Выбор склада
    """
    async with state.proxy() as data:
        if data['sklad'] == 'all':
            if message.text == 'Назад':
                await back(message, state)
            else:
                await bot.send_message(message.from_user.id, '{}'.format(search_art_name(message.text)))
                sklad_list = ['011_825', '012_825', 'A11_825', 'V_Sales', 'RDiff']
                for i in sklad_list:
                    cells = search_all_sklad(message.text, i)
                    if cells:
                        logger.info('Вернул список ячеек - {}: {}'.format(message.text, cells))
                        for item in cells:
                            if i == '012_825':
                                await bot.send_message(message.from_user.id, item,
                                                       reply_markup=InlineKeyboardMarkup(row_width=1).
                                                       add(InlineKeyboardButton(text='Заказать',
                                                                                callback_data='or{}'.format(
                                                                                    message.text))))
                            else:
                                await bot.send_message(message.from_user.id, item)

                    else:
                        await bot.send_message(message.from_user.id, 'Данный артикул отсутствует на складе {}'.
                                               format(i))
                await search(message, state)
        else:
            if message.text == 'Назад':
                await back(message, state)
            else:
                cells = search_articul(message.text, data['sklad'])
                if cells:
                    if len(cells) != 0:
                        logger.info('Вернул список ячеек - {}'.format(cells))
                        for item in cells:
                            if data['sklad'] == '012_825':
                                await bot.send_message(message.from_user.id, item,
                                                       reply_markup=InlineKeyboardMarkup(row_width=1).
                                                       add(InlineKeyboardButton(text='Заказать',
                                                                                callback_data='or{}'.
                                                                                format(message.text))))
                            else:
                                await bot.send_message(message.from_user.id, item)

                else:
                    await bot.send_message(message.from_user.id, 'Данный артикул отсутствует на складе {}'.
                                           format(data['sklad']), reply_markup=second_menu)
                await search(message, state)


@dp.message_handler(content_types=['text'], state=Search.order)
async def order_num(message: types.Message, state: FSMContext):
    num = message.text
    async with state.proxy() as data:
        if num == 'Назад':
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
    await search(message, state)


@dp.message_handler(content_types=['text'], state=Orders.order)
async def order_num(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await back(message, state)
    elif message.text == 'Мой заказ':
        try:
            await bot.send_message(message.from_user.id, 'Ваш заказ!')
            for i in mail(message):
                await bot.send_message(message.from_user.id, i)
        except Exception as ex:
            logger.debug('Заказ пустой({}). Пользователь: {}'.format(ex, message.from_user.id))
            await bot.send_message(message.from_user.id, 'Ваш заказ пуст.')
    elif message.text == 'Отправить Мишке':
        answer = mail(message)
        if len(answer) != 0:
            for i in mail(message):
                await bot.send_message(880277049, 'Пользователь: {} {} отправил Вам:\n{}'.
                                       format(message.from_user.id, message.from_user.first_name, i))
        else:
            await bot.send_message(message.from_user.id, 'Заказ пустой -_-')
    elif message.text == 'Удалить заказ':
        del_orders(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Заказ очищен!')
    else:
        await bot.send_message(message.from_user.id, 'Неверная команда!')


@dp.message_handler(content_types=['text'], state=Place.dowload)
async def search_sklad(message: types.Message, state: FSMContext):
    """Загрузка базы с админки"""
    async with state.proxy() as data:
        sklad_list = ['011_825', '012_825', 'A11_825', 'RDiff', 'V_Sales']
        if message.text in sklad_list:
            data['sklad'] = message.text
            await bot.send_message(message.from_user.id, 'Загрузите файл.')
        elif message.text == 'Назад':
            await back(message, state)
        else:
            await bot.send_message(message.from_user.id, 'Неверно выбран склад.')
            await back(message, state)


@dp.message_handler(content_types=ContentTypes.DOCUMENT,
                    state=[Place.dowload])
async def doc_handler(message: types.Message, state: FSMContext):
    """Ловит документ(EXSEL) и загружает"""
    try:
        async with state.proxy() as data:
            if document := message.document:
                await document.download(
                    destination_file="{}/utils/file_{}.xls".format(path, data['sklad']),
                )
                logger.info('{} - Загружен документ'.format(message.from_user.id))
                await bot.send_message(message.from_user.id, 'Загружен документ на {} склад.'.format(data['sklad']),
                                       reply_markup=InlineKeyboardMarkup().add(
                                           InlineKeyboardButton(text='Загрузить в базу',
                                                                callback_data='{}'.format(data['sklad'])
                                                                )))

    except Exception as ex:
        logger.debug(ex)


@dp.callback_query_handler(state=Place.mesto_1)
async def place_1(call: types.CallbackQuery, state: FSMContext):
    """Поиск по рядам"""
    async with state.proxy() as data:
        if call.data == '012_825-OX':
            data['mesto1'] = call.data
            asyncio.create_task(delete_message(data['message1']))
            await call.message.answer('\n'.join(place('012_825-OX', '012_825')))
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
        else:
            await call.answer(cache_time=5)
            answer_p: str = call.data
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
    answer: str = call.data
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
        await call.message.answer('Список товара на {}:'.format(result))
        data['result'] = result
        logger.info(data['result'])

        if place(result, '012_825'):
            for item in place(result, '012_825'):
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


@dp.callback_query_handler(state=Place.dowload)
async def dow_all_sklads(call: types.CallbackQuery, state: FSMContext):
    """Функция загрузки базы"""
    try:
        dowload(call.data)
        await bot.send_message(call.from_user.id, 'База обновлена', reply_markup=menu_admin)
    except Exception as ex:
        logger.debug(ex)
    finally:
        await state.reset_state()
        logger.info('Очистил state')


@dp.callback_query_handler(state=[Place.mesto_4, Search.show_all])
async def answer_call(call: types.CallbackQuery, state: FSMContext):
    """Кол беки с инлайн кнопок и показ  1 картинки в ячейках"""
    if call.data == 'exit':
        await call.message.answer('Главное меню. Введите артикул. Пример: 80264335', reply_markup=menu)
        await state.reset_state()
        logger.info('Очистил state')
    elif call.data == 'hide':
        async with state.proxy() as data:
            for key in data:
                if str(key).startswith('photo'):
                    asyncio.create_task(delete_message(data['{}'.format(key)]))
    else:
        start_time = time.time()
        logger.info('Пользователь {} запросил картинку на арт.{}'.format(call.from_user.id, call.data))
        if os.path.exists(r"{}/base/json/{}.json".format(path, call.data)):
            logger.info('нашел json и вывел результат')
            with open(r"{}/base/json/{}.json".format(path, call.data), "r", encoding='utf-8') as read_file:
                data_url = json.load(read_file)
                photo = await call.message.answer_photo(data_url["url_imgs"][0],
                                                        reply_markup=hide)
        else:
            with open('{}/stikers/seach.tgs'.format(path), 'rb') as sticker:
                sticker = await call.message.answer_sticker(sticker)
            try:
                data_url = await get_info(call.data)
                photo = await call.message.answer_photo(data_url['url_imgs'][0],
                                                        reply_markup=hide)
            except Exception as ex:
                logger.debug(ex)
            finally:
                asyncio.create_task(delete_message(sticker))

        async with state.proxy() as data:
            try:
                if 'photo{}'.format(call.data) in data:
                    for key in data:
                        if str(key).startswith('photo'):
                            asyncio.create_task(delete_message(data['{}'.format(key)]))

                data['photo{}'.format(call.data)] = photo
            except Exception as ex:
                logger.debug(ex)
        logger.info('Вывод результата через:{} сек.'.format(time.time() - start_time))


@dp.callback_query_handler(state=Search.sklad)
async def input_art(call: types.CallbackQuery, state: FSMContext):
    """
    Поиск по складам введенного артикула
    """
    async with state.proxy() as data:
        if call.data == 'exit':
            await call.message.answer('Главное меню. Введите артикул. Пример: 80264335', reply_markup=menu)
            await state.reset_state()
            logger.info('Очистил state')
        elif call.data.startswith('or'):
            await bot.send_message(call.from_user.id, 'Ввeдите количество:', reply_markup=second_menu)
            data['order'] = call.data[2:]
            await Search.order.set()
        else:
            await bot.send_message(call.from_user.id, 'Введите артикул', reply_markup=second_menu)
            await Search.art.set()
            data['sklad'] = call.data
        asyncio.create_task(delete_message(data['message1']))
        asyncio.create_task(delete_message(data['message2']))


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: Message):
    """Управление голосовыми, пока в разработке"""
    await bot.send_message(message.from_user.id, 'Иди работай')
    voice = message.voice
    await bot.download_file_by_id(voice)


@dp.message_handler(content_types=['text'], state='*')
async def bot_message(message: types.Message, state: FSMContext):
    """
    Выводим сохраненные qcode ячеек, стандартные.
    Основное, парсим через функцию requests_mediagroup, если уже есть json просто выводим инфу,
    иначе идем циклом по кортежу и выводим инф
    """
    if check(message.from_user.id):
        if message.text == '🆚 V-Sales_825':
            await bot.send_message(message.from_user.id, 'V-Sales_825')
            qrc = open('{}/qcodes/V-Sales_825.jpg'.format(path), 'rb')
            await bot.send_photo(message.chat.id, qrc)

        elif message.text == '🗃 011_825-Exit_sklad':
            await bot.send_message(message.from_user.id, '011_825-Exit_sklad')
            qrc = open('{}/qcodes/011_825-Exit_sklad.jpg'.format(path), 'rb')
            await bot.send_photo(message.chat.id, qrc)

        elif message.text == '🤖 Qrcode ячейки':
            await show_qr(message)

        elif message.text == '📦 Содержимое ячейки':
            await show_place(message, state)

        elif message.text == 'ℹ Информация' or message.text == 'Помощь':
            await bot_help(message)

        elif message.text == '📟 Мой заказ':
            await bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=orders)
            await Orders.order.set()

        elif message.text == '🔍 Поиск на складах':
            await search(message, state)

        elif message.text == 'Назад':
            await back(message, state)

        elif message.text == '📖 Любой текст в Qr':
            await bot.send_message(message.from_user.id, 'Введите текст.', reply_markup=second_menu)
            await QR.qr.set()

        elif message.text == 'Отправить':
            await bot.send_message(message.from_user.id, 'Введите сообщения для общей рассылки:',
                                   reply_markup=second_menu)
            await Messages.mes.set()

        elif message.text == 'Загрузка базы':
            await bot.send_message(message.from_user.id, 'Выберите склад', reply_markup=dowload_menu)
            await Place.dowload.set()

        else:
            start_time = time.time()
            answer = message.text.lower()
            logger.info('Пользователь {} {}: запросил артикул {}'.format(
                message.from_user.id,
                message.from_user.first_name,
                answer
            ))

            if len(answer) == 8 and answer.isdigit() and answer[:2] == '80':
                await show_media(message)
            else:
                await bot.send_message(message.from_user.id,
                                       'Неверно указан артикул или его нет на сайте. Пример: 80422781')
            logger.info("--- время выполнения поиска по сайту - {}s seconds ---".format(time.time() - start_time))
    else:
        await helps(message)
        await bot.send_message(message.from_user.id, 'Нет доступа, введите пароль!')
        await Logging.log.set()
