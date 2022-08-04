import asyncio
from ctypes import Union
import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loguru import logger
import csv
import peewee
from peewee import *

from data.config import path
import bot
from database.connect_DB import *
from database.products import Product
from handlers.users.back import back
from handlers.users.delete_message import delete_message
from handlers.users.show_media import show_media
from keyboards.inline.verification import creat_groups_menu, verification_view, verification_check_btn
from loader import dp, bot
from state.states import Verification


async def verification_start(message, state):
    async with state.proxy() as data:
        mes = await bot.send_message(message.from_user.id, 'Выберите группу:', reply_markup=creat_groups_menu())
        await Verification.get_groups.set()
        data['message'] = mes


def create_table():
    dbhandle.connect()
    Product.create_table()
    try:
        with open('{}/utils/file_V_Sales.csv'.format(path), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Физические \nзапасы'] == '1':
                    art = row['Код \nноменклатуры']
                    name = row['Описание товара']
                    group = row['ТГ']
                    temp = Product.create(vendor_code=art, name=name, group=group)
                    temp.save()
    except peewee.InternalError as px:
        print(str(px))
    finally:
        dbhandle.close()
    Product.list()


@dp.callback_query_handler(state=Verification.get_groups)
async def groups(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            try:
                asyncio.create_task(delete_message(data['message']))
            except Exception as ex:
                logger.debug('Нет сообщения для удаления {}'.format(ex))
            data['TG'] = call.data
            if call.data == 'exit':
                await back(call, state)
            else:
                mes = await bot.send_message(call.from_user.id, "Выберите действие:", reply_markup=verification_view)
                await Verification.view_result.set()
                data['message'] = mes

    except Exception as ex:
        logger.debug(ex)


@dp.callback_query_handler(state=Verification.view_result)
async def ver_view(call: types.CallbackQuery, state: FSMContext):
    dbhandle.connect()
    art_dict = {}
    rows = Product.select()
    async with state.proxy() as data:
        try:
            asyncio.create_task(delete_message(data['message']))
        except Exception as ex:
            logger.debug('Нет сообщения для удаления {}'.format(ex))

        for prod in rows:
            if data['TG'] == prod.group:
                art_dict[prod.vendor_code] = [prod.group, prod.status]
        # art_dict = sorted(art_dict)
        dbhandle.close()

        if call.data == 'exit':
            await back(call, state)
        elif call.data == 'start':
            for prod in art_dict.keys():
                if art_dict[prod][1] == 'Не проверен' or art_dict[prod][1] == 'Пропущен':
                    if await while_answer(state) == 'break':
                        await state.reset_state()
                        await state.finish()
                        return
                    flag = False

                    await state.update_data(answer=False)

                    await show_media(call, prod)
                    mes = await bot.send_message(call.from_user.id, "{}\nТовар в наличии?".format(prod),
                                                 reply_markup=verification_check_btn(prod))
                    data['message'] = mes
                    await Verification.check_item.set()

                    while not flag:
                        await asyncio.sleep(1)
                        flag = await while_answer(state)
                    try:
                        asyncio.create_task(delete_message(data['message']))
                    except Exception as ex:
                        logger.debug('Первое сообщение {}'.format(ex))

            await bot.send_message(call.from_user.id, 'Вы завершили проверку')
            await back(call, state)
        else:
            data['list'] = call.data
            await get_list(call, state, art_dict)


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
    art = call.data[4:]
    async with state.proxy() as data:
        if call.data.startswith('yes'):
            await bot.send_message(call.from_user.id, "В наличии")
            update_states(art, "Найден")
        elif call.data.startswith('no'):
            await bot.send_message(call.from_user.id, "Отсутствует")
            update_states(art, "Не найден")
        elif call.data.startswith('skip'):
            await bot.send_message(call.from_user.id, "Вы пропустили позицию")
            update_states(art, "Пропущен")
        elif call.data.startswith('exit'):
            await back(call, state)
        data['answer'] = call.data[:4]
        await data.save()
        await Verification.view_result.set()


def update_states(art: str, new_status: str):
    dbhandle.connect()
    prod = Product.get(Product.vendor_code == art)
    prod.status = new_status
    prod.save()
    dbhandle.close()


async def get_list(call: types.CallbackQuery, state: FSMContext, art_dict):
    try:
        async with state.proxy() as data:
            if call.data == 'all_list':
                await bot.send_message(call.from_user.id, "Весь список товаров данной группы:")
                await show_list(call, state)
            elif call.data == 'skip_list':
                await bot.send_message(call.from_user.id, "Список пропущенного товара:")
                await show_list(call, state, filter=('Пропущен'))
            elif call.data == 'tried_list':
                await bot.send_message(call.from_user.id, "Список проверенного товара:")
                await show_list(call, state, filter=('Найден', 'Не найден'))
            elif call.data == 'not_found_list':
                await bot.send_message(call.from_user.id, "Список не найденного товара:")
                await show_list(call, state, filter=('Не найден'))

    except Exception as ex:
        logger.debug(ex)


async def show_list(call: types.CallbackQuery, state,
                    filter=('Не проверен', 'Пропущен', 'Не найден', 'Найден')):
    dbhandle.connect()
    rows = Product.select()
    art_dict = dict()
    async with state.proxy() as data:
        for prod in rows:
            if data['TG'] == prod.group:
                art_dict[prod.vendor_code] = [prod.group, prod.status]
    dbhandle.close()
    count = 0
    count_all = 0
    product_list = []
    try:
        for key, value in art_dict.items():
            if value[1] in filter:
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
    myfile = '{}/database/mydatabase.db'.format(path)
    if os.path.isfile(myfile):
        os.remove(myfile)
    create_table()
