from aiogram import types
import time
from data.config import path
from database.connect_DB import dbdate
from database.date import *


async def bot_help(message: types.Message):
    """
    Справка бота
    """
    dbdate.connect()
    for i in DateBase.select():
        await message.answer("Последнее обновления базы: \n"
                             "011_825 - {}\n"
                             "012_825 - {}\n"
                             "A11_825 - {}\n"
                             "RDiff - {}\n"
                             "V_Sales - {}\n".format(i.date_011_825, i.date_012_825, i.date_A11_825,
                                                     i.date_RDiff, i.date_V_Sales_new,
                                                     ))
    dbdate.close()
    await message.answer('\nДля показа фотографий товара и цены с сайта'
                         '\nВведите артикул в главном меню. Пример: 80264335.'
                         '\n🤖 Qrcode ячейки - '
                         '\nДля показа Qrcode ячейки на складе. '
                         '\n📦 Содержимое ячейки - '
                         '\nДля показа товара на ячейке.'
                         '\n🔍 Поиск на складах - '
                         '\nДля поиска ячеек, румов и тд. с определенным артикулом.'
                         '\n📖 Любой текст в Qr - '
                         '\nДля преобразования текста в Qrcode(не более 500 символов).'
                         '\n📝Проверка товара - '
                         '\nДля проверки представленности товара и для пополнения.'
                         '\nВыбираете отдел ТДД и количество в зале.'
                         '\nПо всем вопросам обращаться к Михаилу, БЮ 825(склад), \nпочта - muxazila@mail.ru')

    await message.answer_document(open('{}/doc.txt'.format(path), 'rb'))
