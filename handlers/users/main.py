import datetime
import random
import sqlite3
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text, italic, code
from loguru import logger

import bot
from all_requests.parse_action import parse_actions, view_actions
from data.config import ADMINS, PASSWORD, path
from handlers.users.back import back
from handlers.users.cell_content import show_place
from handlers.users.helps import bot_help
from handlers.users.search import search
from handlers.users.show_media import show_media
from handlers.users.show_qrs import show_qr
from handlers.users.stocks_check import start_check_stocks
from keyboards.default import menu
from keyboards.default.menu import second_menu, menu_admin, dowload_menu, orders
from loader import dp, bot
from state.states import Orders
from state.states import Place, Logging, Messages, QR, Action
from utils.check_bd import check
from utils.open_exsel import dowload, search_all_sklad
from utils.read_bd import del_orders, mail


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
    if check(message):
        hello = ['limur.tgs', 'Dicaprio.tgs', 'hello.tgs', 'hello2.tgs', 'hello3.tgs']
        sticker = open('{}/stikers/{}'.format(path, random.choice(hello)), 'rb')
        await bot.send_sticker(message.chat.id, sticker)
        if str(message.from_user.id) in ADMINS:
            await message.answer('Добро пожаловать, {}!'
                                 '\nДля помощи нажми на кнопку Информация(/help)'
                                 .format(message.from_user.first_name),
                                 reply_markup=menu_admin)
        else:
            await message.answer('Добро пожаловать, {}!'
                                 '\nДля помощи нажми на кнопку Информация'
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
async def input_password(message: types.Message, state: FSMContext):
    """
    Если пароль верен, вносит в базу пользователя, перезапускает функуию старт"""
    if message.text == PASSWORD:
        connect = sqlite3.connect('{}/base/BD/users.bd'.format(path))
        cursor = connect.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_id(
        id INTEGER, 
        name TEXT, 
        date REAL, 
        БЮ INTEGER, 
        Black_status INTEGER)
        """)
        connect.commit()

        cursor.execute('SELECT id FROM login_id WHERE id = {}'.format(message.from_user.id))
        data = cursor.fetchone()
        if data is None:
            date = datetime.datetime.now()
            shop = 0
            black = 0
            user_id = [message.from_user.id, message.from_user.first_name, date, shop, black]
            cursor.execute('INSERT INTO login_id VALUES(?,?,?,?,?);', user_id)
            connect.commit()
        await state.reset_state()
        logger.info('Очистил state')
        await bot_start(message)
    else:
        await bot.send_message(ADMINS[0], '{} {}\nНеверно ввел пароль'.format(message.from_user.id,
                                                                              message.from_user.first_name))


@dp.message_handler(content_types=['text'], state=Messages.mes)
async def message_for_users(message: types.Message, state: FSMContext):
    """
    Рассылка сообщения пользователям бота,
    нажатие админ кнопки на "отправить"
    """

    if message.text == 'В главное меню':
        await back(message, state)
    else:
        text_mes = '❗{}❗\n'.format(message.text)
        logger.info('Запустил рассылку - {}  от пользователя {}'.format(text_mes, message.from_user.id))
        connect = sqlite3.connect('{}/base/BD/users.bd'.format(path))
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM login_id;")
        one_result = cursor.fetchall()
        for i in one_result:
            try:
                await bot.send_message(i[0], text_mes)
            except Exception as ex:
                logger.debug('Не удалось отправить сообщение {} {}'.format(i, ex))
        await back(message, state)


@dp.message_handler(content_types=['text'], state=Place.dowload)
async def dowload_base(message: types.Message, state: FSMContext):
    """Загрузка базы ячеек"""
    async with state.proxy() as data:
        sklad_list = ['011_825', '012_825', 'A11_825', 'RDiff', 'V_Sales', 'Мин.витрина']
        if message.text in sklad_list:
            data['sklad'] = message.text
            await bot.send_message(message.from_user.id, 'Загрузите файл.')
        elif message.text == 'В главное меню':
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
        await bot.send_message(message.from_user.id, 'Ошибка при загрузке эксель')
        logger.debug(ex)


@dp.callback_query_handler(state=Place.dowload)
async def dow_all_sklads(call: types.CallbackQuery, state: FSMContext):
    """Функция загрузки базы"""
    try:
        if dowload(call.data):
            await bot.send_message(call.from_user.id, 'База обновлена', reply_markup=menu_admin)
        else:
            await bot.send_message(call.from_user.id, 'Ошибка при записи в csv')
    except Exception as ex:
        logger.debug(ex)
    finally:
        await back(call.message, state)


@dp.message_handler(content_types=[ContentType.STICKER, ContentType.VOICE], state='*')
async def unknown_message(message: types.Message):
    message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await message.reply(message_text, parse_mode=ParseMode.MARKDOWN)
    with open('{}/stikers/fuck.tgs'.format(path), 'rb') as sticker:
        await message.answer_sticker(sticker)


@dp.message_handler(content_types=['text'], state=Orders.order)
async def order_num(message: types.Message, state: FSMContext):
    if message.text == 'В главное меню':
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


@dp.message_handler(content_types=['text'], state='*')
async def bot_message(message: types.Message, state: FSMContext):
    """
    Выводим сохраненные qcode ячеек, стандартные.
    Основное, парсим через функцию requests_mediagroup, если уже есть json просто выводим инфу,
    иначе идем циклом по кортежу и выводим инф
    """
    if check(message) != 3 and check(message):
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

        elif message.text == '📝Проверка товара':
            await start_check_stocks(message, state)

        elif message.text == '🔍 Поиск на складах':
            await search(message, state)

        elif message.text == 'В главное меню':
            await back(message, state)

        elif message.text == '📖 Любой текст в Qr':
            await bot.send_message(message.from_user.id, 'Введите текст.', reply_markup=second_menu)
            await QR.qr.set()

        elif message.text == '💳 Акции':
            await Action.set_group.set()
            await view_actions(message, state)
        elif message.text == 'Обновить Акции':
            try:
                parse_actions()
                await bot.send_message(message.from_user.id, 'Сканирование завершено')
            except Exception as ex:
                await bot.send_message(message.from_user.id, 'Парсер отвалился {}'.format(ex))
            finally:
                await back(message, state)
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
            logger.info(
                'Пользователь {} {}: запросил артикул {}'.format(message.from_user.id, message.from_user.first_name,
                                                                 answer))
            if len(answer) == 8 and answer.isdigit() and answer[:2] == '80':
                await show_media(message)
                sklad_list = ['011_825', '012_825', 'A11_825', 'V_Sales', 'RDiff']
                full_block = ['Остатки на магазине:']
                try:
                    for i in sklad_list:
                        cells = search_all_sklad(message.text, i)
                        if cells:
                            for item in cells:
                                full_block.append(item)
                    await bot.send_message(message.from_user.id, '\n'.join(full_block))
                except Exception as ex:
                    logger.debug('Ошибка при выводе ячеек в гланом меню {}', ex)
                    await bot.send_message(message.from_user.id, 'Данный товар отсутствует.')
            else:
                await bot.send_message(message.from_user.id,
                                       'Неверно указан артикул или его нет на сайте. Пример: 80422781')
            logger.info("--- время выполнения поиска по сайту - {}s seconds ---".format(time.time() - start_time))
    elif check(message) == 3:
        await bot.send_message(message.from_user.id, 'Вы заблокированы')
        with open('{}/stikers/fuck.tgs'.format(path), 'rb') as sticker:
            await message.answer_sticker(sticker)
        logger.info(
            'Заблокированный пользователь {}{} вошел'.format(message.from_user.id, message.from_user.first_name))
    else:
        await helps(message)
        await bot.send_message(message.from_user.id, 'Нет доступа, введите пароль!')
        await Logging.log.set()
