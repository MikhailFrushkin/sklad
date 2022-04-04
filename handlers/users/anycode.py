from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger
from loader import dp


@dp.message_handler(commands='Выбор ячейки')
async def get_any_price(message: types.Message):
    logger.info('Пользователь {}: {} запросил команду /lowprice или  /highprice'.format(
        message.from_user.id,
        message.from_user.username))
