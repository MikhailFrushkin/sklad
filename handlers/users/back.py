from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default import menu
from keyboards.default.menu import menu_admin
from loader import bot


async def back(message, state: FSMContext):
    """Кнопка Назад, скидывает стейты и возвращает в главное меню"""
    if str(message.from_user.id) in ADMINS:
        await bot.send_message(message.from_user.id,
                               'Главное меню.\nВведите артикул. Пример: 80264335',
                               reply_markup=menu_admin)
    else:
        await bot.send_message(message.from_user.id,
                               'Главное меню.\nВведите артикул. Пример: 80264335', reply_markup=menu)
    await state.reset_state()
