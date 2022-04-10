from loguru import logger
from aiogram.dispatcher.filters.builtin import CommandStart
import qrcode
import bot
from keyboards.default import menu
from aiogram import types
from loader import dp, bot
from state.show_photo import Showphoto
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer('Добро пожаловать, {}!'
                         '\nЯ бот - для показа Qcode ячеек склада'
                         '\nвведите ряд, секцию, ячейку без нулей и пробела'.format(message.from_user.first_name))
    await message.answer('Введите или выберите ячейку', reply_markup=menu)


@dp.message_handler(commands=['showphoto'], state='*')
async def show_photo(message: types.Message, state: FSMContext):

    logger.info('Пользователь {}: {} запросил команду /showphoto'.format(
        message.from_user.id,
        message.from_user.username))

    await bot.send_message(message.from_user.id, 'Введите артикул. Пример: 80264335')
    async with state.proxy() as data:
        data['command'] = message.get_command()
        data['message_id'] = message.message_id

    await Showphoto.show.set()


@dp.message_handler(state=Showphoto.show)
async def show(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    try:
        photo = open('photo/{}.jpg.'.format(answer), 'rb')

        await bot.send_photo(message.from_user.id, photo)
    except Exception as ex:
        print(ex)
    finally:
        await state.reset_state()
        logger.info('Очистил state')


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
