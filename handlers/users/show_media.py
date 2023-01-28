import json
import os

from aiogram import types
from loguru import logger

from all_requests.parse_on_requests import parse
from data.config import path
from loader import bot
import random


async def show_media(message, articul):
    try:
        data = parse(articul)
        if data:
            line = data['name']
            for item in data['characteristic']:
                line += '\n{}'.format(item)
            line += '\nЦена с сайта: {} руб.'.format(data['price'])
            await bot.send_message(message.from_user.id, line)
            await bot.send_message(message.from_user.id, 'Упаковка:\n{}'.format('\n'.join(data['box'])))
            try:
                if len(data['pictures']) > 2:
                    count = 0
                    media = types.MediaGroup()
                    for i in data['pictures']:
                        media.attach_photo(types.InputMediaPhoto(i))
                        count += 1
                        if count == 5:
                            break
                    await bot.send_media_group(message.from_user.id, media=media)
                else:
                    await bot.send_photo(message.from_user.id, data['pictures'][0])
            except Exception as ex:
                logger.debug('Первое фото не пошло {}', ex)
                await bot.send_photo(message.from_user.id, data['pictures'][random.randint(1, 3)])
        else:
            if os.path.exists(r"{}\base\json\{}.json".format(path, articul)):
                logger.info('нашел json ')
                with open(r"{}\base\json\{}.json".format(path, articul), 'r', encoding='utf-8') as file:
                    data = json.load(file)
            line = data['name']
            for item in data['characteristic']:
                line += '\n{}'.format(item)
            line += '\nЦена с сайта: {} руб.'.format(data['price'])
            await bot.send_message(message.from_user.id, line)
            try:
                await bot.send_photo(message.from_user.id, data['pictures'][0])
            except Exception as ex:
                logger.debug('Первое фото не пошло {}', ex)
                await bot.send_photo(message.from_user.id, data['pictures'][1])

    except Exception as ex:
        er = 'https://jackwharperconstruction.com/wp-content/uploads/9/c/9/9c980deb1f9f42ef2244b13de3aa118d.jpg'
        await bot.send_photo(message.from_user.id, er)
        logger.debug('{}'.format(ex))
