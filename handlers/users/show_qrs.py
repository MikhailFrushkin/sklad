import os
import os.path
import time

import qrcode
from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

import bot
from handlers.users.back import back
from keyboards.default.menu import qr_menu
from loader import dp, bot
from state.states import Showphoto, QR
from utils.new_qr import qr_code


async def show_qr(message: types.Message):
    """
    Отправляет пользователя в меню qr кодов(кнопок), и генерирует их с ввода.
    """
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
    """
    ans_list = ['011_825-Exit_sklad', '011_825-Exit_zal', '011_825-Exit_Dost', 'V-Sales_825', 'R12_BrakIn_825']
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
                    with open('C:/Users/sklad/qcodes/{}.jpg'.format(message.text), 'rb') as qrcod:
                        await bot.send_photo(message.from_user.id, qrcod)
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
                    qrcod = open('C:/Users/sklad/qcodes/{}.jpg'.format(message.text), 'rb')
                    await bot.send_photo(message.from_user.id, qrcod)

                else:
                    await bot.send_message(message.from_user.id,
                                           'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела')
            else:
                await bot.send_message(message.from_user.id,
                                       'Неверно указана ячейка!Введите ряд, секцию, ячейку без нулей и пробела')

            logger.info('Пользователь {} запросил qr на ячейку: {}'.format(message.from_user.id, ans))
            time.sleep(1)
            os.remove('C:/Users/sklad/qcodes/{}.jpg'.format(ans))
        else:
            await bot.send_message(message.from_user.id, 'Введены буквы или символы')


@dp.message_handler(content_types=['text'], state=QR.qr)
async def gen_qr(message: types.Message, state):
    """Генерация Qrcodre по тексту пользователя"""
    logger.info('Пользователь {} запросил qr на текст: {}'.format(message.from_user.id, message.text))
    data = message.text
    if data == 'Назад':
        await back(message, state)
    else:
        if len(data) > 500:
            await bot.send_message(message.from_user.id, 'Слишком длинный текст.')
            await bot.send_message(message.from_user.id, 'Введите текст.')
            await QR.qr.set()

        else:
            try:
                qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=15)
                qr.add_data(data)
                img = qr.make_image(image_factory=StyledPilImage,
                                    module_drawer=RoundedModuleDrawer(),
                                    color_mask=RadialGradiantColorMask(
                                        back_color=(255, 255, 255),
                                        center_color=(255, 128, 0),
                                        edge_color=(0, 0, 255)))
                img.save('C:/Users/sklad/qcodes/temp.jpg', 'JPEG')
                with open('C:/Users/sklad/qcodes/temp.jpg', 'rb') as qrc:
                    await bot.send_photo(message.chat.id, qrc)
                os.remove('C:/Users/sklad/qcodes/temp.jpg')
            except Exception as ex:
                logger.debug(ex)
