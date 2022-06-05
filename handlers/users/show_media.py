import asyncio
import json
import os

from aiogram import types
from loguru import logger

from all_requests.requests_mediagroup import get_info
from data.config import path
from handlers.users.delete_message import delete_message
from loader import bot


async def show_media(message: types.Message):
    """
    Вывод 3х картинок со ввода артикула в главном меню
    Если есть json выодит инфу, иначе парсит сайт
    """
    answer = message.text.lower()
    if not os.path.exists(r"{}/base/json/{}.json".format(path, answer)):
        try:
            with open('{}/stikers/seach.tgs'.format(path), 'rb') as sticker:
                sticker = await bot.send_sticker(message.chat.id, sticker)

            await get_info(answer)
        except Exception as ex:
            await bot.send_message(message.from_user.id,
                                   'Неверно указан артикул или его нет на сайте. Пример: 80422781')
            logger.debug('{}'.format(ex))
        finally:
            asyncio.create_task(delete_message(sticker))

    try:
        with open(r"{}/base/json/{}.json".format(path, answer), "r", encoding='utf-8') as read_file:
            data = json.load(read_file)
            logger.info('нашел json и вывел результат')
            await bot.send_message(message.from_user.id, data['name'].replace('#', 'Артикул: '))
            if len(data['url_imgs']) > 2:
                media = types.MediaGroup()
                for i in data['url_imgs']:
                    media.attach_photo(i)
                await bot.send_media_group(message.from_user.id, media=media)
            else:
                await message.answer_photo(data['url_imgs'][0])
            await bot.send_message(message.from_user.id,
                                   'Цена с сайта: {}(Уточняйте в Вашем магазине).'.format(data['price']))
            await bot.send_message(message.from_user.id, '\n'.join(data['params']))
            
    except Exception as ex:
        logger.debug(ex)
