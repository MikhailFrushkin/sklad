import asyncio
import json
import os

import requests
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

            data = get_info(answer)
            await bot.send_message(message.from_user.id, data['name'].replace('#', 'Артикул: '))
            good_urls = []
            for url in data['url_imgs']:
                response = requests.head('{}'.format(url))
                if response.status_code < 300:
                    good_urls.append(url)
            if len(good_urls) >= 2:
                media = types.MediaGroup()
                for i in good_urls:
                    media.attach_photo(i)
                await bot.send_media_group(message.from_user.id, media=media)
            else:
                await message.answer_photo(data['url_imgs'][0])
            await bot.send_message(message.from_user.id,
                                   'Цена с сайта: {}(Уточняйте в Вашем магазине).'.format(data['price']))
            # await bot.send_message(message.from_user.id, '\n'.join(data['params']))
        except Exception as ex:
            await bot.send_message(message.from_user.id,
                                   'Неверно указан артикул или его нет на сайте. Пример: 80422781')
            logger.debug('{}'.format(ex))
        finally:
            asyncio.create_task(delete_message(sticker))
    else:
        try:
            with open(r"{}/base/json/{}.json".format(path, answer), "r", encoding='utf-8') as read_file:
                data = json.load(read_file)
                logger.info('нашел json и вывел результат')
                await bot.send_message(message.from_user.id, data['name'].replace('#', 'Артикул: '))
                good_urls = []
                for url in data['url_imgs']:
                    response = requests.head('{}'.format(url))
                    if response.status_code < 300:
                        good_urls.append(url)
                if len(good_urls) >= 2:
                    media = types.MediaGroup()
                    for i in good_urls:
                        media.attach_photo(i)
                    await bot.send_media_group(message.from_user.id, media=media)
                else:
                    await message.answer_photo(good_urls[0])
                await bot.send_message(message.from_user.id,
                                       'Цена с сайта: {}(Уточняйте в Вашем магазине).'.format(data['price']))
                # await bot.send_message(message.from_user.id, '\n'.join(data['params']))

        except Exception as ex:
            logger.debug(ex)
