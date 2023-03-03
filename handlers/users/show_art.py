import time

from loguru import logger

import bot
from data.config import hidden
from handlers.users.show_media import show_media
from loader import bot
from utils.open_exsel import search_all_sklad


async def show_art_in_main_menu(message, answer):
    id_user = message.from_user.id
    logger.info(
        'Пользователь {} {}: запросил артикул {}'.format(id_user, message.from_user.first_name,
                                                         answer))
    sklad_list = ['011_825', '012_825', 'A11_825', 'V_Sales', 'RDiff']
    full_block = ['Остатки на магазине:']
    try:
        if (len(answer) == 8 and answer.isdigit() and answer[:2] == '80') or\
                (len(answer) == 6 and answer.isdigit()):
            if len(answer) == 6:
                answer = '80' + answer
            await show_media(message, answer)
        else:
            await bot.send_message(id_user,
                                   'Неверно указан артикул или его нет на сайте. Пример: 80422781')
    except Exception as ex:
        logger.debug(ex)

    if not hidden():
        try:
            for i in sklad_list:
                cells = search_all_sklad(answer, i)
                if cells:
                    for item in cells:
                        full_block.append(item)
            if len(full_block) > 1:
                await bot.send_message(id_user, '\n'.join(full_block))

        except Exception as ex:
            logger.debug('Ошибка при выводе ячеек в гланом меню {}', ex)
