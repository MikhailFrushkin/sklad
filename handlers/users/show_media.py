from aiogram import types
from loguru import logger

from all_requests.parse_on_requests import parse
from loader import bot


async def show_media(message: types.Message):
    articul = message.text.lower()
    try:
        data = parse(articul)
        logger.info(data)
        line = data['name']
        for item in data['characteristic']:
            line += '\n{} {}'.format(item['name'], item['value'])
        line += '\nЦена с сайта: {} руб.'.format(data['price'])
        await bot.send_message(message.from_user.id, line)
        # if len(data['pictures']) >= 2:
        #     media = types.MediaGroup()
        #     for item in data['pictures']:
        #         print(requests.get(item).status_code)
        #         media.attach_photo(item)
        #     await bot.send_media_group(message.from_user.id, media=media)
        # else:
        #     await message.answer_photo(data['pictures'])
        try:
            await message.answer_photo(data['pictures'][0])
        except Exception as ex:
            logger.debug('Первое фото не пошло {}', ex)
            await message.answer_photo(data['pictures'][1])
    except Exception as ex:
        await bot.send_message(message.from_user.id,
                               'Неверно указан артикул или его нет на сайте. Пример: 80422781')
        logger.debug('{}'.format(ex))
