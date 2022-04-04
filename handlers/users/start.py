from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import qrcode

import bot
from keyboards.default import menu
from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer('Добро пожаловать, {}!'
                         '\nЯ бот - для показа Qcode ячеек склада'
                         '\nвведите ряд, секцию, ячейку без нулей и пробела'.format(message.from_user.first_name))
    await message.answer('Введите или выберите ячейку', reply_markup=menu)


@dp.message_handler()
async def bot_message(message: types.Message):

    if message.text == 'VSL':
        await bot.send_message(message.from_user.id, 'vls')

        qrc = open('V_Sales-825.jpg', 'rb')
        await bot.send_photo(message.chat.id, qrc)

    elif message.text == 'Brak':
        await bot.send_message(message.from_user.id, 'Доделаю когда-нибудь -)')
    else:
        ans = message.text
        if len(ans) == 3:
            if int(ans[1]) < 9 and int(ans[2]) < 5:

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
                await bot.send_message(message.from_user.id, 'Неверно указана ячейка!')
        elif len(ans) == 4 and int(ans[0]) == 1:
            if int(ans[2]) < 9 and int(ans[3]) < 5:

                await bot.send_message(message.from_user.id, '{}{} ряд {} секция {} ячейка'.
                                       format(ans[0], ans[1], ans[2], ans[3]))

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data('012_825-0{}{}-0{}-{}'
                            .format(message.text[0], message.text[1], message.text[2], message.text[3]))
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img.save('qcodes/{}.jpg'.format(message.text), 'JPEG')
                qrc = open('qcodes/{}.jpg'.format(message.text), 'rb')
                await bot.send_photo(message.chat.id, qrc)
            else:
                await bot.send_message(message.from_user.id, 'Неверно указана ячейка!')
        else:
            await bot.send_message(message.from_user.id, 'Неверно указана ячейка!')