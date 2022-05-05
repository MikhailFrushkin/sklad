import asyncio
import json
import os

from aiogram import types
from loguru import logger

from all_requests.requests_mediagroup import get_info
from handlers.users.delete_message import delete_message
from loader import bot


async def show_media(message: types.Message):
    """
    Вывод 3х картинок со ввода артикула в главном меню
    Если есть json выодит инфу, иначе парсит сайт
    """
    answer = message.text.lower()
    if os.path.exists('base/{}.json'.format(answer)):
        logger.info('нашел json и вывел результат')
        with open('base/{}.json'.format(answer), "r", encoding='utf-8') as read_file:
            data = json.load(read_file)
            await bot.send_message(message.from_user.id, data['name'].replace('#', 'Артикул: '))
            if len(data['url_imgs']) >= 2:
                media = types.MediaGroup()
                if len(data['url_imgs']) < 10:
                    for i_photo in data['url_imgs']:
                        media.attach_photo(i_photo)
                    await message.answer_media_group(media)
                else:
                    for i_photo in range(10):
                        media.attach_photo(data['url_imgs'][i_photo])
                    await message.answer_media_group(media)
            else:
                await message.answer_photo(data['url_imgs'])
            await bot.send_message(message.from_user.id, '\n'.join(data['params']))
            await bot.send_message(message.from_user.id,
                                   'Цена с сайта: {}(Уточняйте в Вашем магазине).'.format(data['price']))
    else:
        try:
            with open('stikers/seach.tgs', 'rb') as sticker:
                sticker = await bot.send_sticker(message.chat.id, sticker)

            url_list = get_info(answer)
            await bot.send_message(message.from_user.id, url_list[1].replace('#', 'Артикул: '))
            logger.info('Функция вернула список урл - {}\n'.format(url_list))
            if len(url_list[0]) >= 2:
                media = types.MediaGroup()
                if len(url_list[0]) < 10:
                    for i_photo in url_list[0]:
                        media.attach_photo(i_photo)
                    await message.answer_media_group(media)
                else:
                    for i_photo in range(10):
                        media.attach_photo(url_list[0][i_photo])
                    await message.answer_media_group(media)
            else:
                await message.answer_photo(url_list[0][0])
            await bot.send_message(message.from_user.id, '\n'.join(url_list[2]))
            await bot.send_message(message.from_user.id,
                                   'Цена с сайта: {}(Уточняйте в Вашем магазине).'.format(url_list[3]))
        except Exception as ex:
            await bot.send_message(message.from_user.id,
                                   'Неверно указан артикул или его нет на сайте. Пример: 80422781')
            logger.debug('{}'.format(ex))
        finally:
            asyncio.create_task(delete_message(sticker))
