import random
import sqlite3
import time

import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text, italic, code
from loguru import logger

import bot
from all_requests.parse_action import parse_actions, view_actions
from data.config import ADMINS, PASSWORD, path, hidden
from database.date import *
from database.products import NullProduct
from database.users import Users, Keyboard, Operations
from handlers.users.Verification import verification_start, create_table2
from handlers.users.back import back
from handlers.users.cell_content import show_place
from handlers.users.delete_message import delete_message
from handlers.users.edit_keyboard import inlane_edit_keyboard, create_keyboard
from handlers.users.helps import bot_help
from handlers.users.info_rdiff import read_all_base, new_rdiff_to_exsel
from handlers.users.search import search
from handlers.users.show_art import show_art_in_main_menu
from handlers.users.show_qrs import show_qr
from handlers.users.sold_product import read_base_vsl
from handlers.users.stocks_check import start_check_stocks, save_exsel_pst, creat_pst, union_art
from keyboards.default import menu
from keyboards.default.menu import second_menu, menu_admin, dowload_menu
from keyboards.inline.graf import graf_check
from loader import dp, bot
from state.states import Orders, Graf, EditKeyboard
from state.states import Place, Logging, Messages, QR, Action
from utils.check_bd import check
from utils.open_exsel import dowload
from utils.read_bd import del_orders, mail
from utils.read_image import read_image


async def say_ib(message, state):
    await bot.send_message(message.from_user.id,
                           'Функция недоступна, возможно через некоторое время(пару лет) сотрудники '
                           'ИБ позволят нам пользоваться '
                           'функционалом, который мало того что удобен, так и местами в '
                           '5 раз быстрее способствует выполнению текущих бизнес-процессов')
    await back(message, state)


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
            try:
                await message.answer('Добро пожаловать, {}!'
                                     '\nДля помощи нажми на кнопку Информация(/help)'
                                     .format(message.from_user.first_name),
                                     reply_markup=create_keyboard(message.from_user.id))
            except Exception as ex:
                await message.answer('Добро пожаловать, {}!'
                                     '\nДля помощи нажми на кнопку Информация(/help)'
                                     .format(message.from_user.first_name),
                                     reply_markup=menu)
                logger.debug(message.from_user.first_name, ex)
    else:
        await helps(message)
        await bot.send_message(message.from_user.id, 'Нет доступа, введите пароль!')
        await Logging.log.set()


@dp.message_handler(commands=['keyboard'], state='*')
async def keyboard_user(message: types.Message, state: FSMContext):
    """Команда для редактирования главного меню"""
    await state.reset_state()
    await state.finish()
    async with state.proxy() as data:
        message_k = await bot.send_message(message.from_user.id, 'Выберите кнопки меню:',
                                           reply_markup=inlane_edit_keyboard(message.from_user.id))
        await EditKeyboard.edit.set()
        data['mes'] = message_k


@dp.callback_query_handler(state=EditKeyboard.edit)
async def keyboard(call: types.CallbackQuery, state: FSMContext):
    """смена буливого при нажатии на клавиши ,какую кнопку показывать в меню или нет"""
    async with state.proxy() as data:
        try:
            query = Users.get(Users.id_tg == call.from_user.id)
            await delete_message(data['mes'])
            if call.data == 'exit':
                await back(call, state)
            else:
                if call.data == 'vsales':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.vsales:
                        new_s.keyboard.vsales = False
                    else:
                        new_s.keyboard.vsales = True
                    new_s.keyboard.save()

                if call.data == 'ex_sklad':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.ex_sklad:
                        new_s.keyboard.ex_sklad = False
                    else:
                        new_s.keyboard.ex_sklad = True
                    new_s.keyboard.save()

                if call.data == 'qr_cell':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.qr_cell:
                        new_s.keyboard.qr_cell = False
                    else:
                        new_s.keyboard.qr_cell = True
                    new_s.keyboard.save()

                if call.data == 'text_qr':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.text_qr:
                        new_s.keyboard.text_qr = False
                    else:
                        new_s.keyboard.text_qr = True
                    new_s.keyboard.save()

                if call.data == 'text_qr':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.text_qr:
                        new_s.keyboard.text_qr = False
                    else:
                        new_s.keyboard.text_qr = True
                    new_s.keyboard.save()

                if call.data == 'content':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.content:
                        new_s.keyboard.content = False
                    else:
                        new_s.keyboard.content = True
                    new_s.keyboard.save()

                if call.data == 'search':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.search:
                        new_s.keyboard.search = False
                    else:
                        new_s.keyboard.search = True
                    new_s.keyboard.save()

                if call.data == 'check':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.check:
                        new_s.keyboard.check = False
                    else:
                        new_s.keyboard.check = True
                    new_s.keyboard.save()

                if call.data == 'buy':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.buy:
                        new_s.keyboard.buy = False
                    else:
                        new_s.keyboard.buy = True
                    new_s.keyboard.save()

                if call.data == 'check_one':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.check_one:
                        new_s.keyboard.check_one = False
                    else:
                        new_s.keyboard.check_one = True
                    new_s.keyboard.save()

                if call.data == 'stock':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.stock:
                        new_s.keyboard.stock = False
                    else:
                        new_s.keyboard.stock = True
                    new_s.keyboard.save()

                if call.data == 'info':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.info:
                        new_s.keyboard.info = False
                    else:
                        new_s.keyboard.info = True
                    new_s.keyboard.save()

                if call.data == 'tel':
                    new_s = Users.get(Users.id_tg == call.from_user.id)
                    if query.keyboard.tel:
                        new_s.keyboard.tel = False
                    else:
                        new_s.keyboard.tel = True
                    new_s.keyboard.save()
                message_k = await bot.send_message(call.from_user.id, 'Выберите кнопки меню:',
                                                   reply_markup=inlane_edit_keyboard(call.from_user.id))
                data['mes'] = message_k
        except Exception as ex:
            print(ex)


@dp.message_handler(commands=['help'], state='*')
async def helps(message: types.Message):
    """
    Справка бота
    """
    await bot_help(message)


@dp.message_handler(content_types=['photo'], state='*')
async def handle_docs_photo(message):
    logger.info('фото загруженно')
    await message.photo[-1].download(f'{path}/photos/фото_{message.from_user.id}.jpg')
    operation = Operations(user_id=Users.get(id_tg=message.from_user.id), operation="Закинул изображение в главное меню")
    operation.save()
    art_list = read_image(f'{path}/photos/фото_{message.from_user.id}.jpg')
    if not art_list:
        await bot.send_message(message.from_user.id, f'Не найдено артикулов на фото')
    for art in art_list:
        if not art.startswith('80'):
            art = list(art)
            art[0] = '8'
            art[1] = '0'
            art = ''.join(art)
        await bot.send_message(message.from_user.id, f'Артикул: {art}')
        await show_art_in_main_menu(message, art)
        time.sleep(0.5)


@dp.message_handler(content_types=['text'], state=Logging.log)
async def input_password(message: types.Message, state: FSMContext):
    """
    Если пароль верен, вносит в базу пользователя, перезапускает функуию старт"""
    if message.text == PASSWORD:
        keyboards = Keyboard()
        keyboards.save()
        new_user = Users(id_tg=message.from_user.id, name=message.from_user.first_name, keyboard=keyboards)
        new_user.save()
        await state.reset_state()
        logger.info('Очистил state')
        await bot_start(message)
    else:
        await bot.send_message(ADMINS[0], '{} {}\nНеверно ввел пароль'.format(message.from_user.id,
                                                                              message.from_user.first_name))


@dp.message_handler(content_types=['text', 'document', 'photo'], state=Messages.mes)
async def message_for_users(message: types.Message, state: FSMContext):
    """
    Рассылка сообщения пользователям бота,
    нажатие админ кнопки на "отправить"
    """

    if message.text == 'В главное меню':
        await back(message, state)
    else:
        users = Users.select()
        if document := message.document:
            try:
                logger.info('{} - Загружен документ'.format(message.from_user.id))
                media_list = ['png', 'jpg', 'jpeg']
                ex = document.file_name.split('.')[-1]
                if ex in media_list:
                    await document.download(
                        destination_file="{}/files/file.{}".format(path, ex),
                    )

                    for user in users:
                        try:
                            with open("{}/files/file.{}".format(path, ex), 'rb') as photo:
                                await bot.send_photo(user.id_tg, photo=photo)
                        except Exception as exp:
                            logger.debug('Не удалось отправить фото {} {}'.format(user.id_tg, exp))
                    await back(message, state)

                else:
                    await document.download(
                        destination_file="{}/files/file.{}".format(path, ex),
                    )
                    for user in users:
                        try:
                            await bot.send_document(user.id_tg, document=open("{}/files/file.{}".format(path, ex), 'rb'))

                        except Exception as exp:
                            logger.debug('Не удалось отправить сообщение {} {}'.format(user.id_tg, exp))
                    await back(message, state)


            except Exception as ex:
                logger.debug(ex)
        elif photo := message.photo:
            try:
                print('Загрузка фото')
                await message.photo[-1].download("{}/files/file.png".format(path))
                for user in users:
                    try:
                        with open("{}/files/file.png".format(path), 'rb') as photo:
                            await bot.send_photo(user.id_tg, photo=photo)
                    except Exception as exp:
                        logger.debug('Не удалось отправить сообщение {} {}'.format(user.id_tg, exp))
                await back(message, state)
            except Exception as ex:
                logger.debug(ex)
        else:
            text_mes = '❗{}❗\n'.format(message.text)
            logger.info('Запустил рассылку - {}  от пользователя {}'.format(text_mes, message.from_user.id))

            for user in users:
                try:
                    await bot.send_message(user.id_tg, text_mes)
                except Exception as ex:
                    logger.debug('Не удалось отправить сообщение {} {}'.format(user.id_tg, ex))
            await back(message, state)


@dp.message_handler(content_types=['text'], state=Place.dowload)
async def dowload_base(message: types.Message, state: FSMContext):
    """Загрузка базы ячеек"""
    async with state.proxy() as data:
        sklad_list = ['011_825', '012_825', 'A11_825', 'RDiff', 'V_Sales', 'S_825']
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
            try:
                if os.path.exists('{}/files/file_old_{}.xlsx'.format(path, data['sklad'])):
                    os.remove('{}/files/file_old_{}.xlsx'.format(path, data['sklad']))
                old_name = '{}/files/file_{}.xlsx'.format(path, data['sklad'])
                mtime = os.path.getmtime(old_name)
                date_old = time.ctime(mtime)
                os.rename(old_name, '{}/files/file_old_{}.xlsx'.format(path, data['sklad']))
                dowload('old_{}'.format(data['sklad']))
                myfile = '{}/database/DateBase.db'.format(path)
                if data['sklad'] == 'V_Sales':
                    if os.path.isfile(myfile):
                        for i in DateBase.select():
                            i.date_V_Sales_old = date_old
                            i.save()
                    else:
                        DateBase.create_table()
                        temp = DateBase.create(date_V_Sales_old=date_old)
                        temp.save()
                        logger.info('создал бд')
                elif data['sklad'] == 'RDiff':
                    if os.path.isfile(myfile):
                        for i in DateBase.select():
                            i.date_RDiff_old = date_old
                            i.save()
                    else:
                        DateBase.create_table()
                        temp = DateBase.create(date_RDiff_old=date_old)
                        temp.save()
                        logger.info('создал бд')
            except Exception as ex:
                logger.debug(ex)
            await dowload_exs(message, state)

    except Exception as ex:
        await bot.send_message(message.from_user.id, 'Ошибка при загрузке эксель {}'.format(ex))
        logger.debug(ex)


async def dowload_exs(message, state):
    async with state.proxy() as data:
        if document := message.document:
            await document.download(
                destination_file="{}/files/file_{}.xlsx".format(path, data['sklad']),
            )
            logger.info('{} - Загружен документ'.format(message.from_user.id))
            await bot.send_message(message.from_user.id, 'Загружен документ на {} склад.'.format(data['sklad']),
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(text='Загрузить в базу',
                                                            callback_data='{}'.format(data['sklad'])
                                                            )))
        mtime = os.path.getmtime("{}/files/file_{}.xlsx".format(path, data['sklad']))
        date_new = time.ctime(mtime)
        myfile = '{}/database/DateBase.db'.format(path)
        if not os.path.isfile(myfile):
            DateBase.create_table()
            logger.info('создал бд')
        for i in DateBase.select():
            if data['sklad'] == 'V_Sales':
                i.date_V_Sales_new = date_new
            elif data['sklad'] == '011_825':
                i.date_011_825 = date_new
            elif data['sklad'] == '012_825':
                i.date_012_825 = date_new
            elif data['sklad'] == 'A11_825':
                i.date_A11_825 = date_new
            elif data['sklad'] == 'RDiff':
                i.date_RDiff = date_new
            i.save()


@dp.callback_query_handler(state=Place.dowload)
async def dow_all_sklads(call: types.CallbackQuery, state: FSMContext):
    """Функция загрузки базы"""
    try:
        async with state.proxy() as data:
            if dowload(call.data):
                await bot.send_message(call.from_user.id, 'База обновлена', reply_markup=menu_admin)
                if data['sklad'] == 'V_Sales':
                    try:
                        try:
                            read_base_vsl()
                        except Exception as ex:
                            logger.debug(ex)
                        await bot.send_message(call.from_user.id, 'Обновлен файл с проданным товаром')
                        NullProduct.create_table()
                        try:
                            save_exsel_pst(creat_pst())
                        except Exception as ex:
                            logger.debug(ex)
                        groups_list = ['11', '20', '21', '22', '23', '25', '28', '35']
                        data_nulls = dict()
                        products = []
                        for group in groups_list:
                            dict_art_012 = union_art('012_825', group)[1]
                            dict_art_v = union_art('V_Sales', group)[1]
                            dict_art_s = union_art('S_825', group)[1]
                            for key in dict_art_012.keys():
                                if key not in dict_art_v.keys() and key not in dict_art_s.keys():
                                    products.append(key)
                            data_nulls[group] = products
                            products = []

                        for key, value in data_nulls.items():
                            try:
                                row = NullProduct.get(NullProduct.group == key)
                                row.num = len(value)
                                row.save()
                            except Exception:
                                temp = NullProduct.create(group=key, num=len(value))
                                temp.save()
                        await bot.send_message(call.from_user.id,
                                               'Невыставленный товар:\nТекстиль: {}\nВанная комната: {}\nШторы: '
                                               '{}\nПосуда: {}\nДекор: {}\nХимия, хранение, ковры: {}\n'
                                               'Прихожая: {}\n'
                                               'Свет {}\n'
                                               .format(
                                                   len(data_nulls['11']),
                                                   len(data_nulls['20']),
                                                   len(data_nulls['21']),
                                                   len(data_nulls['22']),
                                                   len(data_nulls['23']),
                                                   len(data_nulls['28']),
                                                   len(data_nulls['35']),
                                                   len(data_nulls['25']),
                                               ))
                    except Exception as ex:
                        logger.debug(ex)


            else:
                await bot.send_message(call.from_user.id, 'Ошибка при записи в csv')
    except Exception as ex:
        logger.debug(ex)
    finally:
        await back(call, state)


@dp.message_handler(content_types=[ContentType.STICKER], state='*')
async def unknown_message(message: types.Message):
    message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await message.reply(message_text, parse_mode=ParseMode.MARKDOWN)
    with open('{}/stikers/fuck.tgs'.format(path), 'rb') as sticker:
        await message.answer_sticker(sticker)


@dp.message_handler(content_types=[ContentType.VOICE], state='*')
async def voice_message_handler(message: types.Message):
    import uuid
    import os
    try:
        import speech_recognition as sr
    except ModuleNotFoundError as ex:
        logger.debug(ex)

    logger.info("Пользователь {} {} отправил голосовое".format(message.from_user.id,
                                                               message.from_user.first_name))
    filename = str(uuid.uuid4())
    file_name_full = f"{path}/files/voice/" + filename + ".ogg"
    file_name_full_converted = f"{path}/files/voice/" + filename + ".wav"
    file_info = await bot.get_file(message.voice.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())
    os.system("ffmpeg -i " + file_name_full + " " + file_name_full_converted)
    try:
        r = sr.Recognizer()
        with sr.AudioFile(file_name_full_converted) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text, language='ru-RU')
                await bot.send_message(message.from_user.id, "{}".format(text))
                result = read_art(text)
                logger.info("Вернул текстовое сообщение {}".format(result))
                await show_art_in_main_menu(message, result)
            except Exception as ex:
                result = "Sorry.. run again..."
                logger.debug(ex)
    except Exception as ex:
        logger.debug(ex)
    await bot.send_message(message.from_user.id, "{}".format(result))
    os.remove(file_name_full)
    os.remove(file_name_full_converted)


def read_art(text_s):
    import re
    text_s = text_s.replace(' ', '').replace(",", "")
    pattern = "\d{8,}"
    result = re.search(pattern, text_s)[0][:8]
    return result


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
    operation_user = message.text
    comment = ''
    id = message.from_user.id
    if check(message) != 3 and check(message):
        if message.text == '🆚V-Sales_825':
            await bot.send_message(id, 'V-Sales_825')
            qrc = open('{}/qcodes/V-Sales_825.jpg'.format(path), 'rb')
            logger.info('Пользователь {} {} открыл QR V-Sales_825'.format(id, message.from_user.first_name))
            await bot.send_photo(message.chat.id, qrc)

        elif message.text == '🗃011_825-Exit_sklad':
            await bot.send_message(id, '011_825-Exit_sklad')
            qrc = open('{}/qcodes/011_825-Exit_sklad.jpg'.format(path), 'rb')
            logger.info('Пользователь {} {} открыл QR 011_825-Exit_sklad'.format(id, message.from_user.first_name))
            await bot.send_photo(message.chat.id, qrc)

        elif message.text == '🤖Qrcode ячейки':
            logger.info('Пользователь {} {} открыл QR ячейки'.format(id, message.from_user.first_name))
            await show_qr(message)

        elif message.text == '📦Содержимое ячейки':
            if not hidden():
                await show_place(message, state)
            else:
                await say_ib(message, state)

        elif message.text == 'ℹИнформация' or message.text == 'Помощь':
            logger.info('Пользователь {} {} нажал help'.format(id, message.from_user.first_name))
            await bot_help(message)

        elif message.text == 'Телефоны':
            try:
                excel_data_df = pd.read_excel('{}/Телефоны.xlsx'.format(path))
                excel_data_df.to_csv('{}/Телефоны.scv'.format(path))
                with open('{}/Телефоны.scv'.format(path), newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    line = []
                    for row in reader:
                        line.append('{} - {}'.format(row['Должность'], str(row['Номер телефона']).replace('.', ',')))
                    await bot.send_message(id, '\n'.join(line), reply_markup=second_menu)
                    await message.answer_document(open('{}/График.xls'.format(path), 'rb'), reply_markup=graf_check)
                    await Graf.check_graf.set()

            except Exception as ex:
                logger.debug(ex)
            finally:
                os.remove('{}/Телефоны.scv'.format(path))

        elif message.text == '📑Проверка единичек':
            if not hidden():
                logger.info('Пользователь {} {} нажал Проверка единичек'.format(id, message.from_user.first_name))
                await verification_start(message, state)
            else:
                await say_ib(message, state)


        elif message.text == '📝Проверка товара':
            if not hidden():
                data_nulls_res = {}
                try:
                    data_nulls = NullProduct.select()
                    data_time = DateBase.select()
                    for key in data_nulls:
                        data_nulls_res[key.group] = key.num

                    await bot.send_message(message.from_user.id,
                                           '{}\n'
                                           'Невыставленный товар:\nТекстиль: {}\nВанная комната: {}\nШторы: '
                                           '{}\nПосуда: {}\nДекор: {}\nХимия, хранение, ковры: {}\n'
                                           'Прихожая: {}\nСвет: {}\n'.format(
                                               *[i.date_V_Sales_new for i in data_time],
                                               data_nulls_res['11'],
                                               data_nulls_res['20'],
                                               data_nulls_res['21'],
                                               data_nulls_res['22'],
                                               data_nulls_res['23'],
                                               data_nulls_res['28'],
                                               data_nulls_res['35'],
                                               data_nulls_res['25'],
                                           ))
                    await start_check_stocks(message, state)
                except Exception as ex:
                    logger.debug(ex)
            else:
                await say_ib(message, state)

        elif message.text == '💰Проданный товар':
            if not hidden():
                logger.info('Пользователь {} {} нажал Проданный товар'.format(id, message.from_user.first_name))
                await bot.send_message(id,
                                       'В доработке, т.к. стали принимать на весло, '
                                       'некорректное движение теперь, с весла на склад и т.д.'
                                       '\nВ свободное время допилю)')
                for i in DateBase.select():
                    await bot.send_message(id, 'Проданный товар и доступность на складе\n'
                                               'с {}\n'
                                               'по {}.'.format(i.date_V_Sales_old, i.date_V_Sales_new))
                await message.answer_document(open('{}/files/sold.xlsx'.format(path), 'rb'))
            else:
                await say_ib(message, state)


        elif message.text == '🔍Поиск по наименованию':
            if not hidden():
                await search(message, state)
            else:
                await say_ib(message, state)

        elif message.text == 'В главное меню':
            await back(message, state)

        elif message.text == '📖Любой текст в Qr':
            await bot.send_message(id, 'Введите текст.', reply_markup=second_menu)
            await QR.qr.set()

        elif message.text == '💳Акции':
            await Action.set_group.set()
            await view_actions(message, state)

        elif message.text == 'Обновить Акции':
            try:
                parse_actions()
                await bot.send_message(id, 'Сканирование завершено')
            except Exception as ex:
                await bot.send_message(id, 'Парсер отвалился {}'.format(ex))
            finally:
                await back(message, state)

        elif message.text == 'Отправить':
            await bot.send_message(id, 'Введите сообщения для общей рассылки:',
                                   reply_markup=second_menu)
            await Messages.mes.set()

        elif message.text == 'Загрузка базы':
            await bot.send_message(id, 'Выберите склад', reply_markup=dowload_menu)
            await Place.dowload.set()
        elif message.text == 'Сброс единичек':
            await create_table2(message)
        elif message.text == '🤬Новые Рдиффы':
            if not hidden():
                logger.info('Пользователь {} {} нажал Новые рдиффы'.format(id, message.from_user.first_name))
                for i in DateBase.select():
                    await bot.send_message(id, 'Новые рдиффы\n'
                                               'с {}\n'
                                               'по {}.'.format(i.date_RDiff_old, i.date_RDiff))
                await message.answer_document(open('{}/files/new_rdiff.xlsx'.format(path), 'rb'))
            else:
                await say_ib(message, state)
        elif message.text == 'Обновить новые рдиффы':
            read_all_base()
            new_rdiff_to_exsel()
            await bot.send_message(id, 'Рдиффы обновленны')
        elif message.text == 'Сники мод' and message.from_user.id in [int(i) for i in ADMINS]:
            if hidden():
                with open('{}/files/hidden.txt'.format(path), 'w', encoding='utf-8') as f:
                    f.write('False')
                await bot.send_message(id, 'Выключен')
            else:
                with open('{}/files/hidden.txt'.format(path), 'w', encoding='utf-8') as f:
                    f.write('True')
                await bot.send_message(id, 'Включен')
        elif message.text == 'Статистика' and message.from_user.id in [int(i) for i in ADMINS]:
            mes = []
            query = (Users
                     .select(Users, fn.COUNT(Operations.id).alias('Operations_count'))
                     .join(Operations, JOIN.LEFT_OUTER)
                     .group_by(Users.id))
            for user in query:
                mes.append('{} {} - запросов: {}'.format(user.id_tg, user.name, user.Operations_count))
            await bot.send_message(message.from_user.id, '\n'.join(mes))
        else:
            operation_user = "Запросил артикул в главном меню"
            comment = message.text
            answer = message.text.lower()
            await show_art_in_main_menu(message, answer)
        if not Operations.table_exists():
            Operations.create_table()
            logger.debug('Таблицы созданы успешно.')
        operation = Operations(user_id=Users.get(id_tg=message.from_user.id), operation=operation_user, comment=comment)
        operation.save()
        for admin in ADMINS:
            if message.from_user.id not in [int(i) for i in ADMINS]:
                await bot.send_message(admin, '{} {} {}'.
                                       format(message.text, message.from_user.id, message.from_user.first_name))
    elif check(message) == 3:
        await bot.send_message(id, 'Вы заблокированы')
        with open('{}/stikers/fuck.tgs'.format(path), 'rb') as sticker:
            await message.answer_sticker(sticker)
        logger.info(
            'Заблокированный пользователь {}{} пытался войти'.format(id,
                                                                     message.from_user.first_name))
        for admin in ADMINS:
            await bot.send_message(admin,
                                   'Заблокированный пользователь {}{} пытался войти'.
                                   format(id,
                                          message.from_user.first_name))
    else:
        await helps(message)
        await bot.send_message(message.from_user.id, 'Нет доступа, введите пароль!')
        await Logging.log.set()
