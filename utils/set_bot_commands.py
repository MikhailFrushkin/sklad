from aiogram import types


async def set_default_commands(dp):
    """команды бота в меню"""
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'),
            types.BotCommand('showqr', 'Показать qrcode'),
            types.BotCommand('graph', ' Показать график работы')
        ]
    )
