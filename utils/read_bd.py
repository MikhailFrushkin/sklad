import sqlite3

from loguru import logger

from data.config import path
from loader import bot
from utils.open_exsel import search_articul_order


def get_bd_info(id):
    """чтение бд"""
    try:
        con = sqlite3.connect(r'{}/base/BD/users.bd'.format(path))
        with con:
            cursor = con.cursor()

            sql_select_query = """select * from orders where id = ?"""
            cursor.execute(sql_select_query, (id,))
            records = cursor.fetchall()
            data = dict()
            order_list = []
            for row in records:
                data["ID"] = row[0]
                data["Артикул"] = row[1]
                data["Количество"] = row[2]
                order_list.append([data['Артикул'], data['Количество']])
        logger.info('Заказ прочитан')
        return order_list
    except sqlite3.Error as error:
        logger.info("Ошибка при работе с SQLite: {}".format(error))


def set_order(id: int, art: int, num: int):
    """Создание строк с айди, артикул и количество для заказа"""
    try:
        con = sqlite3.connect(r'{}/base/BD/users.bd'.format(path))
        with con:
            cursor = con.cursor()
            con.execute("""CREATE TABLE IF NOT EXISTS orders (id INTEGER, articul INTEGER, num INTEGER)""")
            con.commit()
            data = cursor.fetchone()
            temp = [id, art, num]
            if data is None:
                cursor.execute('INSERT INTO orders VALUES(?,?,?);', temp)
                con.commit()
                logger.info('Заказ записан')
    except sqlite3.Error as error:
        logger.info("Ошибка при работе с SQLite: {}".format(error))


def del_orders(id: int):
    """Удаление заказа по айди пользователя"""
    try:
        con = sqlite3.connect(r'{}/base/BD/users.bd'.format(path))
        with con:
            cursor = con.cursor()

            sql_select_query = """select * from orders where id = ?"""
            cursor.execute(sql_select_query, (id,))
            cursor.execute('DELETE FROM orders WHERE id={}'.format(id))
            logger.info('Заказ удален')
    except sqlite3.Error as error:
        logger.info("Ошибка при работе с SQLite: {}".format(error))


def mail(message):
    try:
        list_places = []
        all_list = []
        result = []

        orders_art = get_bd_info(message.from_user.id)
        orders_art2 = []
        for i in orders_art:
            if i not in orders_art2:
                orders_art2.append([i[0], 0])
        for i in orders_art2:
            for j in orders_art:
                if i[0] == j[0]:
                    i[1] += j[1]
        orders_art3 = []
        for i in orders_art2:
            if i not in orders_art3:
                orders_art3.append(i)
        try:
            for item in orders_art3:
                r = search_articul_order(str(item[0]), '012_825')
                if r:
                    for i in r:
                        if i['Местоположение'] not in list_places:
                            list_places.append(i['Местоположение'])
                    all_list.append(r)
            list_places = sorted(list_places)
        except Exception as ex:
            logger.debug(ex)

        art_dict_list = []
        art_dict = {
            'Код': '',
            'Заказ': 0,
            'Подобранно': 0
        }
        for item in orders_art3:
            art_dict['Код'] = item[0]
            art_dict['Заказ'] = int(item[1])
            art_dict['Подобранно'] = 0
            art_dict_list.append(art_dict)
        try:
            for place in list_places:
                line = '⚠{}'.format(place)
                try:
                    for item in orders_art3:
                        if item[1] > 0:
                            for i in all_list:
                                for j in range(len(i)):
                                    if i[j]['Местоположение'] == place:
                                        if str(item[0]) == i[j]['Код']:
                                            if i[j]['Код'] not in line:
                                                if int(i[j]['Доступно']) >= item[1]:
                                                    line = line + '\n✅ {}\n{} \nДоступно:{} К заказу:{}'. \
                                                        format(i[j]['Код'],
                                                               i[j]['Описание товара'],
                                                               i[j]['Доступно'],
                                                               item[1])
                                                else:
                                                    line = line + '\n✅ {}\n{} \nДоступно:{} К заказу:{}'. \
                                                        format(i[j]['Код'],
                                                               i[j]['Описание товара'],
                                                               i[j]['Доступно'],
                                                               i[j]['Доступно'])
                                                item[1] -= int(i[j]['Доступно'])
                    if len(line) > 20:
                        result.append(line)
                except Exception as ex:
                    logger.debug(ex)
        except Exception as ex:
            logger.debug(ex)
        return result
    except Exception as ex:
        logger.debug(ex)
