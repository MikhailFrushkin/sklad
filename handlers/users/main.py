import asyncio
import datetime
import json
import os.path
import sqlite3
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes
from loguru import logger

import bot
from all_requests.requests_mediagroup import get_info
from data.config import ADMINS
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from handlers.users.helps import bot_help
from handlers.users.search import search
from handlers.users.show_media import show_media
from handlers.users.show_place import show_place
from keyboards.default import menu
from keyboards.default.menu import second_menu, menu_admin, dowload_menu, qr_menu
from keyboards.inline.mesto import mesto2, mesto3, hide, mesto1
from loader import dp, bot
from state.states import Showphoto, Place, Search
from utils.check_bd import check
from utils.new_qr import qr_code
from utils.open_exsel import place, search_articul, dowload, search_all_sklad, search_art_name, place_dost


@dp.message_handler(commands=['start'], state='*')
async def bot_start(message: types.Message):
    """
    Старт бота
    """
    connect = sqlite3.connect('C:/Users/sklad/base/BD/users.bd')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(id INTEGER, name TEXT, date REAL)""")
    connect.commit()

    cursor.execute('SELECT id FROM login_id WHERE id = {}'.format(message.from_user.id))
    data = cursor.fetchone()
    if data is None:
        date = datetime.datetime.now()
        user_id = [message.chat.id, message.from_user.first_name, date]
        cursor.execute('INSERT INTO login_id VALUES(?,?,?);', user_id)
        connect.commit()
    if str(message.from_user.id) in ADMINS:
        await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре',
                             reply_markup=menu_admin)
    else:
        sticker = open('stikers/AnimatedSticker2.tgs', 'rb')
        await bot.send_sticker(message.chat.id, sticker)
        await message.answer('Добро пожаловать, {}!'
                             '\nДля показа фотографий товара, описания и цены с сайта'
                             '\nВведите артикул. Пример: 80264335.'
                             '\n"🤖 Показать Qrcode ячейки" - '
                             '\nДля показа Qrcode ячейки на складе. '
                             '\n"📦 Содержимое ячейки" - '
                             '\nДля показа товара на ячейке.'
                             '\n"🔍 Поиск на складе" - '
                             '\nДля поиска ячеек, румов и тд. с определенным артикулом.'
                             .format(message.from_user.first_name), reply_markup=menu)


@dp.message_handler(commands=['help'], state='*')
async def helps(message: types.Message):
    """
    Справка бота
    """
    await bot_help(message)


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

    await bot.send_message(message.from_user.id, 'Для показа Qrcode введите ряд, секцию,'
                                                 '\nячейку без нулей и пробела.'
                                                 '\nПример: 721 - это 7 ряд 2 секция 1 ячейка',
                           reply_markup=qr_menu)
    await Showphoto.show_qr.set()


@dp.message_handler(state=Showphoto.show_qr)
async def showqr(message: types.Message, state: FSMContext):
    """
    Функция отправки qcodes.
    Ели сообщение удовлетворяет условию, генерирует код и отправляет.
    Скидывает стате.
    """
    ans_list = ['011_825-exit_sklad', '011_825-exit_zal', '011_825-exit_Dost', 'V_Sales_825', 'R12_BrakIn_825']
    ans = message.text
    if ans == 'Назад':
        await back(message, state)
    elif ans in ans_list:
        await bot.send_message(message.from_user.id, '{}'.format(ans))
        qrc = open('C:/Users/sklad/qcodes/{}.jpg'.format(ans), 'rb')
        await bot.send_photo(message.chat.id, qrc)
    else:
        if ans.isdigit():
            if len(ans) == 3:
                if 0 < int(ans[1]) < 9 and int(ans[2]) < 5:

                    await bot.send_message(message.from_user.id, '{} ряд {} секция {} ячейка'.
                                           format(ans[0], ans[1], ans[2]))

                    data = ('012_825-0{}-0{}-{}'.format(message.text[0], message.text[1], message.text[2]))
                    qr_code(message, data)
                    qrcod = open('qcodes/{}.jpg'.format(message.text), 'rb')
                    await bot.send_photo(message.from_user.id, qrcod)
                    logger.info(data)
                else:
                    await bot.send_message(message.from_user.id,
                                           'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела')
            elif len(ans) == 4 and int(ans[0]) == 1 and int(ans[1]) < 8:
                if 0 < int(ans[2]) < 9 and int(ans[3]) < 5:

                    await bot.send_message(message.from_user.id, '{}{} ряд {} секция {} ячейка'.
                                           format(ans[0], ans[1], ans[2], ans[3]))

                    data = ('012_825-{}{}-0{}-{}'
                            .format(message.text[0], message.text[1], message.text[2], message.text[3]))

                    qr_code(message, data)
                    qrcod = open('qcodes/{}.jpg'.format(message.text), 'rb')
                    await bot.send_photo(message.from_user.id, qrcod)

                else:
                    await bot.send_message(message.from_user.id,
                                           'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела')
            else:
                await bot.send_message(message.from_user.id,
                                       'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела')
        else:
            await bot.send_message(message.from_user.id, 'Введены буквы или символы')


@dp.callback_query_handler(state=Search.sklad)
async def input_art(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == 'exit':
            await call.message.answer('Главное меню. Введите артикул. Пример: 80264335', reply_markup=menu)
            await state.reset_state()
            logger.info('Очистил state')
        else:
            await bot.send_message(call.from_user.id, 'Введите артикул', reply_markup=second_menu)
            await Search.art.set()
            data['sklad'] = call.data
        asyncio.create_task(delete_message(data['message1']))
        asyncio.create_task(delete_message(data['message2']))


@dp.message_handler(content_types=['text'], state=Search.art)
async def search_sklad(message: types.Message, state: FSMContext):
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
                        logger.info('Вернул список ячеек - {}'.format(cells))
                        for item in cells:
                            await bot.send_message(message.from_user.id, item)

                    else:
                        await bot.send_message(message.from_user.id, 'Данный артикул отсутствует на складе {}'.
                                               format(i), reply_markup=second_menu)
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
                            await bot.send_message(message.from_user.id, item)

                else:
                    await bot.send_message(message.from_user.id, 'Данный артикул отсутствует на складе {}'.
                                           format(data['sklad']), reply_markup=second_menu)
                await search(message, state)


@dp.message_handler(content_types=['text'], state=Place.dowload)
async def search_sklad(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        sklad_list = ['011_825', '012_825', 'A11_825', 'RDiff', 'V_Sales']
        if message.text in sklad_list:
            data['sklad'] = message.text
            await bot.send_message(message.from_user.id, 'Загрузите файл')
        elif message.text == 'Назад':
            await back(message, state)
        else:
            await bot.send_message(message.from_user.id, 'Неверно выбран склад')
            await back(message, state)


@dp.message_handler(content_types=ContentTypes.DOCUMENT,
                    state=[Place.dowload])
async def doc_handler(message: types.Message, state: FSMContext):
    try:

        async with state.proxy() as data:
            if document := message.document:
                await document.download(
                    destination_file="C:/Users/sklad/utils/file_{}.xls".format(data['sklad']),
                )
                logger.info('{} - Загружен документ'.format(message.from_user.id))
                await bot.send_message(message.from_user.id, 'Загружен документ на {} склад'.format(data['sklad']),
                                       reply_markup=InlineKeyboardMarkup().add(
                                           InlineKeyboardButton(text='Загрузить в базу',
                                                                callback_data='{}'.format(data['sklad'])
                                                                )))

    except Exception as ex:
        logger.debug(ex)


@dp.callback_query_handler(state=Place.mesto_1)
async def place_1(call: types.CallbackQuery, state: FSMContext):
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
                    await bot.send_message(call.from_user.id, 'В ячейках нет отказаного товара')
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
            answer: str = call.data
            logger.info('Получил ряд: {}'.format(answer))
            asyncio.create_task(delete_message(data['message1']))
            mes1 = await call.message.answer('Выберите секцию:', reply_markup=mesto2)
            data['mesto1'] = answer
            data['message1'] = mes1
            await Place.mesto_2.set()


@dp.callback_query_handler(state=Place.mesto_2)
async def place_2(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    answer: str = call.data
    logger.info('Получил секцию: {}'.format(answer))

    async with state.proxy() as data:
        asyncio.create_task(delete_message(data['message1']))
        mes1 = await call.message.answer('Выберите ячейку:', reply_markup=mesto3)
        data['mesto2'] = answer
        data['message1'] = mes1

    await Place.mesto_3.set()


@dp.callback_query_handler(state=Place.mesto_3)
async def place_3(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    answer: str = call.data
    logger.info('Получил ячейку: {}. '.format(answer))

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
async def dow_012(call: types.CallbackQuery, state: FSMContext):
    try:
        dowload(call.data)
        await bot.send_message(call.from_user.id, 'База обновлена', reply_markup=menu_admin)
    except Exception as ex:
        logger.debug(ex)
    finally:
        await state.reset_state()
        logger.info('Очистил state')


@dp.callback_query_handler(state=[Place.mesto_4, Search.show_all])
async def answer_exit(call: types.CallbackQuery, state: FSMContext):
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
        if os.path.exists('base/{}.json'.format(call.data)):
            logger.info('нашел json и вывел результат')
            with open('base/{}.json'.format(call.data), "r", encoding='utf-8') as read_file:
                data = json.load(read_file)
                photo = await call.message.answer_photo(data["url_imgs"][0],
                                                        reply_markup=hide)
        else:
            with open('stikers/seach.tgs', 'rb') as sticker:
                sticker = await call.message.answer_sticker(sticker)
            try:
                url = get_info(call.data)
                photo = await call.message.answer_photo(url[0][0],
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


@dp.message_handler(content_types=['text'], state='*')
async def bot_message(message: types.Message, state: FSMContext):
    """
    Выводим сохраненные qcode ячеек, стандартные.
    Основное, парсим через функцию requests_mediagroup, если уже есть json просто выводим инфу,
    иначе идем циклом по кортежу и выводим инф
    """
    if message.text == '🆚 V-Sales_825':
        await bot.send_message(message.from_user.id, 'V-Sales_825')
        qrc = open('qcodes/V_Sales_825.jpg', 'rb')
        await bot.send_photo(message.chat.id, qrc)

    elif message.text == '🗃 011_825-exit_sklad':
        await bot.send_message(message.from_user.id, '011_825-exit_sklad')
        qrc = open('qcodes/011_825-exit_sklad.jpg', 'rb')
        await bot.send_photo(message.chat.id, qrc)

    elif message.text == '🤖 Qrcode ячейки':
        await show_qr(message, state)

    elif message.text == '📦 Содержимое ячейки':
        await show_place(message, state)

    elif message.text == 'ℹ Информация' or message.text == 'Помощь':
        await bot_help(message)

    elif message.text == '🔍 Поиск на складе':
        await search(message, state)

    elif message.text == 'Назад':
        await back(message, state)

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
        logger.info("--- время выполнения функции - {}s seconds ---".format(time.time() - start_time))
