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
        await bot.send_message(message.from_user.id, 'Доделаю завтра')


    else:
        await bot.send_message(message.from_user.id, '{}'.format(message.text))

        str_answer = message.text
        if not len(str_answer) == 3:
            await bot.send_message(message.from_user.id, 'Неверно указана ячейка!')
        else:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data('012_825-0{}-0{}-{}'.format(message.text[0], message.text[1], message.text[2]))
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save('{}.jpg'.format(message.text), 'JPEG')
            qrc = open('{}.jpg'.format(message.text), 'rb')
            await bot.send_photo(message.chat.id, qrc)
