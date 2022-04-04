from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer('Добро пожаловать, {}!'
                         '\nЯ бот - для создания Qcode ячеек склада'
                         '\nДля вызова справки введите /help'.format(message.from_user.first_name))
    await message.answer('Выберите действие', reply_markup=menu)



