from loguru import logger

from handlers.users.back import back
from handlers.users.helps import bot_help
from keyboards.default.menu import second_menu
from keyboards.inline.mesto import mesto1
from loader import bot
from state.show_photo import Place


async def show_place(message, state):
    ans = message.text
    if ans == 'Назад':
        await back(message, state)
    elif ans == 'Помощь':
        await bot_help(message)
    else:
        logger.info('Пользователь {}: {} {} запустил просмотр ячеек'.format(
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.username
        ))

        await bot.send_message(message.from_user.id, 'Данные на 15.04.22\nВыберите ряд:', reply_markup=second_menu)
        mes1 = await bot.send_message(message.from_user.id, 'Выберите ряд:', reply_markup=mesto1)
        async with state.proxy() as data:
            data['command'] = message.get_command()
            data['message_id'] = message.message_id
            data['message1'] = mes1

        await Place.mesto_1.set()
