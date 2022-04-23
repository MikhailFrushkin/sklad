from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from data.config import ADMINS
from keyboards.default import menu
from keyboards.default.menu import menu_admin


async def back(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        logger.info('Нажата кнопка назад')
        await message.answer('Главное меню.\nВведите артикул. Пример: 80264335', reply_markup=menu_admin)
        await state.reset_state()
        logger.info('Очистил state')
    else:
        logger.info('Нажата кнопка назад')
        await message.answer('Главное меню.\nВведите артикул. Пример: 80264335', reply_markup=menu)
        await state.reset_state()
        logger.info('Очистил state')