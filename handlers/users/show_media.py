import asyncio
import json
import os

from aiogram import types
from loguru import logger

from all_requests.new_parser import get_info
from all_requests.parse_on_requests import parse
from data.config import path
from handlers.users.delete_message import delete_message
from loader import bot


async def show_media(message, articul):

    try:
        data = parse(articul)
        if data:
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
        else:
            if os.path.exists(r"{}\base\json\{}.json".format(path, articul)):
                logger.info('нашел json ')
                with open(r"{}\base\json\{}.json".format(path, articul), 'r', encoding='utf-8') as file:
                    data = json.load(file)

            else:
                with open('{}/stikers/seach.tgs'.format(path), 'rb') as sticker:
                    sticker = await bot.send_sticker(message.chat.id, sticker)
                    data = get_info(articul)
                    logger.info(data)
                    asyncio.create_task(delete_message(sticker))
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
        asyncio.create_task(delete_message(sticker))
        er = 'https://jackwharperconstruction.com/wp-content/uploads/9/c/9/9c980deb1f9f42ef2244b13de3aa118d.jpg'
        await bot.send_photo(message.from_user.id, er)
        logger.debug('{}'.format(ex))
