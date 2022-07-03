from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from data.config import ADMINS
from keyboards.default import menu
from keyboards.default.menu import menu_admin


async def back(message: types.Message, state: FSMContext):
    """Кнопка Назад, скидывает стейты и возвращает в главное меню"""
    if str(message.from_user.id) in ADMINS:
        await message.answer('Главное меню.\nВведите артикул. Пример: 80264335', reply_markup=menu_admin)
        await state.reset_state()
    else:
        await message.answer('Главное меню.\nВведите артикул. Пример: 80264335', reply_markup=menu)
        await state.reset_state()
