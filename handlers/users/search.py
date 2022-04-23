from loguru import logger

from keyboards.default.menu import second_menu
from keyboards.inline.mesto import search_sklad
from loader import bot
from state.show_photo import Search


async def search(message, state):
    logger.info('\nПользователь {}: {} {} запустил поиск на складе'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username
    ))
    mes1 = await bot.send_message(message.from_user.id, '🔍',
                                  reply_markup=second_menu)
    mes2 = await bot.send_message(message.from_user.id, 'Выберите склад:',
                                  reply_markup=search_sklad)
    async with state.proxy() as data:
        data['message1'] = mes1
        data['message2'] = mes2

    await Search.sklad.set()
