import time

from loguru import logger

import bot
from handlers.users.show_media import show_media
from loader import bot
from utils.open_exsel import search_all_sklad


async def show_art_in_main_menu(message, answer):
    id = message.from_user.id
    start_time = time.time()

    logger.info(
        'Пользователь {} {}: запросил артикул {}'.format(id, message.from_user.first_name,
                                                         answer))
    try:
        if len(answer) == 8 and answer.isdigit() and answer[:2] == '80':
            await show_media(message, answer)
            sklad_list = ['011_825', '012_825', 'A11_825', 'V_Sales', 'RDiff']
            full_block = ['Остатки на магазине:']
            try:
                for i in sklad_list:
                    cells = search_all_sklad(answer, i)
                    if cells:
                        for item in cells:
                            full_block.append(item)
                if len(full_block) > 1:
                    await bot.send_message(id, '\n'.join(full_block))
                else:
                    await bot.send_message(id, 'Данный товар отсутствует.')
            except Exception as ex:
                logger.debug('Ошибка при выводе ячеек в гланом меню {}', ex)

        else:
            await bot.send_message(id,
                                   'Неверно указан артикул или его нет на сайте. Пример: 80422781')
        logger.info("--- время выполнения поиска по сайту - {}s seconds ---".format(time.time() - start_time))
    except Exception as ex:
        logger.debug(ex)