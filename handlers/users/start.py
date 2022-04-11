import asyncio
from contextlib import suppress

import qrcode
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from loguru import logger

import bot
from keyboards.default import menu
from loader import dp, bot
from requests_mediagroup import get_photo
from state.show_photo import Showphoto


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    sticker = open('stikers/AnimatedSticker.tgs', 'rb')
    await bot.send_sticker(message.chat.id, sticker)
    await message.answer('Добро пожаловать, {}!'
                         '\nЯ бот - для показа Qrcode ячеек склада и изображений товара'
                         '\nДля показа Qrcode введите ряд, секцию, ячейку без нулей и пробела'
                         '\nДля показа фото нажмите на "Показать артикул"'.format(message.from_user.first_name))
    await message.answer('Введите или выберите ячейку', reply_markup=menu)


@dp.message_handler(commands=['showphoto'], state='*')
async def show_photo(message: types.Message, state: FSMContext):
    logger.info('Пользователь {}: {} {} запросил команду /showphoto'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username
    ))

    await bot.send_message(message.from_user.id, 'Введите артикул. Пример: 80264335')
    async with state.proxy() as data:
        data['command'] = message.get_command()
        data['message_id'] = message.message_id

    await Showphoto.show.set()


@dp.message_handler(state=Showphoto.show)
async def show(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if len(answer) == 8 and answer.isdigit() and answer[:2] == '80':
        try:
            with open('stikers/seach.tgs', 'rb') as sticker:
                sticker = await bot.send_sticker(message.chat.id, sticker)

            url_list = get_photo(answer)
            await bot.send_message(message.from_user.id, url_list[1].replace('#', 'Артикул: '))

            logger.info('Функция вернула список урл - {}'.format(url_list))
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
                await message.answer_photo(url_list)
            asyncio.create_task(delete_message(sticker))

            await state.reset_state()
            logger.info('Очистил state')

        except Exception as ex:
            await bot.send_message(message.from_user.id, 'Неверно указан артикул')
            asyncio.create_task(delete_message(sticker))
            await show_photo(message, state)
            print(ex)
    else:
        await bot.send_message(message.from_user.id, 'Неверно указан артикул')
        await show_photo(message, state)


@dp.message_handler(content_types=['text'], state='*')
async def bot_message(message: types.Message, state: FSMContext):
    if message.text == 'V-Sales_825':
        await bot.send_message(message.from_user.id, 'V-Sales_825')

        qrc = open('qcodes/V-Sales_825.jpg', 'rb')
        await bot.send_photo(message.chat.id, qrc)

    elif message.text == 'R12_BrakIn_825':
        await bot.send_message(message.from_user.id, 'R12_BrakIn_825')

        qrc = open('qcodes/R12_BrakIn_825.jpg', 'rb')
        await bot.send_photo(message.chat.id, qrc)

    elif message.text == 'Показать артикул':
        await show_photo(message, state)

    else:
        ans = message.text
        if ans.isdigit():
            if len(ans) == 3:
                if 0 < int(ans[1]) < 9 and int(ans[2]) < 5:

                    await bot.send_message(message.from_user.id, '{} ряд {} секция {} ячейка'.
                                           format(ans[0], ans[1], ans[2]))

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data('012_825-0{}-0{}-{}'.format(message.text[0], message.text[1], message.text[2]))
                    qr.make(fit=True)

                    img = qr.make_image(fill_color="black", back_color="white")
                    img.save('qcodes/{}.jpg'.format(message.text), 'JPEG')
                    qrc = open('qcodes/{}.jpg'.format(message.text), 'rb')
                    await bot.send_photo(message.chat.id, qrc)
                else:
                    await bot.send_message(message.from_user.id,
                                           'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела')
            elif len(ans) == 4 and int(ans[0]) == 1 and 0 < int(ans[1]) < 8:
                if 0 < int(ans[2]) < 9 and int(ans[3]) < 5:

                    await bot.send_message(message.from_user.id, '{}{} ряд {} секция {} ячейка'.
                                           format(ans[0], ans[1], ans[2], ans[3]))

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data('012_825-{}{}-0{}-{}'
                                .format(message.text[0], message.text[1], message.text[2], message.text[3]))
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    img.save('qcodes/{}.jpg'.format(message.text), 'JPEG')
                    qrc = open('qcodes/{}.jpg'.format(message.text), 'rb')
                    await bot.send_photo(message.chat.id, qrc)
                else:
                    await bot.send_message(message.from_user.id,
                                           'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела')
            else:
                await bot.send_message(message.from_user.id,
                                       'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела')
        else:
            await bot.send_message(message.from_user.id, 'Многа букафф')
