import asyncio
import datetime
import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from data.config import path
import bot
from database.connect_DB import *
from database.products import Product
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from handlers.users.show_media import show_media
from keyboards.inline.verification import creat_groups_menu, verification_view, verification_check_btn, \
    verification_edited_status
from loader import dp, bot
from state.states import Verification


async def verification_start(message, state):
    async with state.proxy() as data:
        mes = await bot.send_message(message.from_user.id, 'Выберите группу:', reply_markup=creat_groups_menu())
        await Verification.get_groups.set()
        data['message'] = mes


async def create_table(message):
    await bot.send_message(message.from_user.id, 'Количество единичек на V_sales: {}'.format(Product.update_bot()))


@dp.callback_query_handler(state=Verification.get_groups)
async def groups(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            try:
                asyncio.create_task(delete_message(data['message']))
            except Exception as ex:
                logger.debug('Нет сообщения для удаления {}'.format(ex))

            dbhandle.connect()
            art_dict = {}
            rows = Product.select().order_by(Product.minigroup_name)
            data['TG'] = call.data
            for prod in rows:
                if data['TG'] == prod.group:
                    art_dict[prod.vendor_code] = [prod.group, prod.status, prod.minigroup_name, prod.place]
            dbhandle.close()

            if call.data == 'exit':
                await back(call, state)
            elif call.data == 'stat':
                dbhandle.connect()
                all_art = 0
                chek_ok = 0
                chek_no = 0
                chek_false = 0

                file = '{}/database/mydatabase.db'.format(path)
                c_timestamp = os.path.getctime(file)
                c_datestamp = datetime.datetime.fromtimestamp(c_timestamp).strftime("%A, %B %e, %H:%M")
                for item in Product.select():
                    all_art += 1
                    if item.status == 'Найден' or item.status == 'Не найден':
                        chek_ok += 1
                        if item.status == 'Не найден':
                            chek_no += 1
                    else:
                        chek_false += 1
                dbhandle.close()
                await bot.send_message(call.from_user.id, 'Статистика\n'
                                                          'Дата обновления файла с единичками:\n'
                                                          '{}\n'
                                                          'Общее кол-во единичек: {}\n'
                                                          'Проверенные: {}\n'
                                                          'Не найденные: {}\n'
                                                          'Не проверенные: {}\n'.format(c_datestamp,
                                                                                        all_art, chek_ok, chek_no,
                                                                                        chek_false))
            else:
                mes = await bot.send_message(call.from_user.id, "Выберите действие:", reply_markup=verification_view)
                await Verification.view_result.set()
                data['dict'] = art_dict
                data['message'] = mes

    except Exception as ex:
        logger.debug(ex)


@dp.callback_query_handler(state=Verification.view_result)
async def ver_view(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        try:
            asyncio.create_task(delete_message(data['message']))
        except Exception as ex:
            logger.debug('Нет сообщения для удаления {}'.format(ex))

        if call.data == 'exit':
            await back(call, state)
        elif call.data == 'start':
            for prod in data['dict'].keys():
                if data['dict'][prod][1] == 'Не проверен' or data['dict'][prod][1] == 'Пропущен':
                    if await while_answer(state) == 'break':
                        return

                    flag = False
                    await state.update_data(answer=False)

                    await show_media(call, prod)
                    mes = await bot.send_message(call.from_user.id, "Ячейка: {}\nАртикул: {}\nТовар в наличии?".format(
                        data['dict'][prod][3], prod), reply_markup=verification_check_btn(prod))
                    data['message'] = mes
                    await Verification.check_item.set()

                    while not flag:
                        await asyncio.sleep(2)
                        flag = await while_answer(state)
                    try:
                        asyncio.create_task(delete_message(data['message']))
                    except Exception as ex:
                        logger.debug('Первое сообщение {}'.format(ex))

            await bot.send_message(call.from_user.id, 'Вы завершили проверку')
            await back(call, state)
        elif call.data == 'edided':
            await bot.send_message(call.from_user.id, 'Введите артикул для редактирования:')
            await Verification.edited_status.set()
        else:
            data['list'] = call.data
            await asyncio.sleep(1)
            await get_list(call, state)


@dp.message_handler(content_types=['text'], state=Verification.edited_status)
async def edidet_art(message: types.Message, state: FSMContext):
    art = message.text
    dbhandle.connect()
    query = Product.select().where(Product.vendor_code == int(art))
    if query.exists():
        async with state.proxy() as data:
            data['edidet'] = art
            await bot.send_message(message.from_user.id, 'Выберите новый статус:',
                                   reply_markup=verification_edited_status)
            await Verification.edited_status_art.set()
    else:
        await bot.send_message(message.from_user.id, 'Неправильно введен артикул')
        dbhandle.close()
        await bot.send_message(message.from_user.id, 'Введите артикул для редактирования:')
        await Verification.edited_status.set()
    dbhandle.close()


@dp.callback_query_handler(state=Verification.edited_status_art)
async def get_items(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        dbhandle.connect()
        art = data['edidet']
        status = Product.get(Product.vendor_code == int(art))
        if call.data == 'ok':
            status.status = 'Найден'
        elif call.data == 'no':
            status.status = 'Не найден'
        elif call.data == 'skip_s':
            status.status = 'Пропущен'
        elif call.data == 'exit':
            await back(call, state)
        else:
            logger.info('edited_status_art неверный колл')
        status.save()
        dbhandle.close()
        await back(call, state)


async def while_answer(state: FSMContext):
    async with state.proxy() as data:
        list_answer = ['yess', 'nooo', 'skip']
        try:
            if data['answer'] in list_answer:
                return True
            elif data['answer'] == 'exit':
                return 'break'
            else:
                return False
        except KeyError as ex:
            logger.debug(ex)


@dp.callback_query_handler(state=Verification.check_item)
async def get_items(call: types.CallbackQuery, state: FSMContext):
    try:
        art = int(call.data[4:])
    except ValueError as ex:
        art = 0
        logger.debug(ex)
    async with state.proxy() as data:
        import collections
        import datetime
        [last] = collections.deque(data['dict'], maxlen=1)
        if call.data.startswith('yes'):
            await bot.send_message(call.from_user.id, "В наличии")
            data['dict'][art][1] = 'Найден'
        elif call.data.startswith('no'):
            await bot.send_message(call.from_user.id, "Отсутствует")
            data['dict'][art][1] = 'Не найден'
        elif call.data.startswith('skip'):
            await bot.send_message(call.from_user.id, "Вы пропустили позицию")
            data['dict'][art][1] = 'Пропущен'
        elif call.data.startswith('exit'):
            dbhandle.connect()
            for key, value in data['dict'].items():
                status = Product.get(Product.vendor_code == int(key))
                if status.status != value[1]:
                    status.status = value[1]
                    status.user_id = call.from_user.id
                    status.updated_at = datetime.datetime.now()
                    status.save()
            dbhandle.close()
            await back(call, state)
        if last == art:
            for key, value in data['dict'].items():
                status = Product.get(Product.vendor_code == int(key))
                status.status = value[1]
                status.save()
            dbhandle.close()
        data['answer'] = call.data[:4]
        await data.save()
        await Verification.view_result.set()


async def get_list(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            if call.data == 'all_list':
                await bot.send_message(call.from_user.id, "Весь список товаров данной группы:")
                await show_list(call, state)
            elif call.data == 'skip_list':
                await bot.send_message(call.from_user.id, "Список пропущенного товара:")
                await show_list(call, state, filters=('Пропущен'))
            elif call.data == 'tried_list':
                await bot.send_message(call.from_user.id, "Список проверенного товара:")
                await show_list(call, state, filters=('Найден', 'Не найден'))
            elif call.data == 'not_found_list':
                await bot.send_message(call.from_user.id, "Список не найденного товара:")
                await show_list(call, state, filters=('Не найден'))
    except Exception as ex:
        logger.debug(ex)


@dp.callback_query_handler(state=Verification.view_result)
async def show_list(call: types.CallbackQuery, state,
                    filters=('Не проверен', 'Пропущен', 'Не найден', 'Найден')):
    dbhandle.connect()
    rows = Product.select()
    art_dict = dict()
    async with state.proxy() as data:
        for prod in rows:
            if data['TG'] == prod.group:
                art_dict[prod.vendor_code] = [prod.group, prod.status]
    dbhandle.close()

    async with state.proxy() as data:
        count = 0
        count_all = 0
        product_list = []
        try:
            for key, value in art_dict.items():
                if value[1] in filters:
                    if count != 25:
                        count += 1
                        count_all += 1
                        product_list.append('{} Группа:{} {}'.format(
                            key,
                            value[0],
                            value[1]))
                    else:
                        await bot.send_message(call.from_user.id, '\n'.join(product_list))
                        count = 0
                        product_list = []
            await bot.send_message(call.from_user.id, '\n'.join(product_list))
            await bot.send_message(call.from_user.id, 'Всего позиций: {}'.format(count_all))
        except Exception as ex:
            await bot.send_message(call.from_user.id, 'Всего позиций: 0')
            logger.debug("Пустое сообщение {}".format(ex))
        await Verification.get_groups.set()
        await groups(call, state)


if __name__ == '__main__':
    pass