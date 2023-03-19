import time

from aiogram.dispatcher import FSMContext
from loguru import logger

from data.config import ADMINS
from handlers.users.edit_keyboard import create_keyboard
from keyboards.default import menu
from keyboards.default.menu import menu_admin
from loader import bot


async def back(message, state: FSMContext):
    """Кнопка Назад, скидывает стейты и возвращает в главное меню"""
    if str(message.from_user.id) in [i for i in ADMINS]:
        await bot.send_message(message.from_user.id,
                               'Главное меню.\nВведите артикул. Пример: 80264335',
                               reply_markup=menu_admin)
    else:
        try:
            await bot.send_message(message.from_user.id,
                                   'Главное меню.\nВведите артикул. Пример: 80264335',
                                   reply_markup=create_keyboard(message.from_user.id))
        except Exception as ex:
            await message.answer('Добро пожаловать, {}!'
                                 '\nДля помощи нажми на кнопку Информация(/help)'
                                 .format(message.from_user.first_name),
                                 reply_markup=menu)
            logger.debug(message.from_user.first_name, ex)

    await state.reset_state()
    await state.finish()


# async def spam():
#     while True:
#         await bot.send_message(1099191065, '☺️☺️Пошел нахуй☺️☺️ 1099191065 Сергей')
#         time.sleep(1)
#
#
# if __name__ == '__main__':
#     await spam()