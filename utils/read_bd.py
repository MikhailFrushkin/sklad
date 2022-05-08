import sqlite3

from loguru import logger

from loader import bot
from utils.open_exsel import search_articul_order


def get_bd_info(id):
    """чтение бд"""
    try:
        con = sqlite3.connect(r'C:\Users\sklad\base\BD\users.bd')
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
        return order_list
    except sqlite3.Error as error:
        logger.info("Ошибка при работе с SQLite: {}".format(error))


def set_order(id: int, art: int, num: int):
    """Создание строк с айди, артикул и количество для заказа"""
    try:
        con = sqlite3.connect(r'C:\Users\sklad\base\BD\users.bd')
        with con:
            cursor = con.cursor()
            con.execute("""CREATE TABLE IF NOT EXISTS orders (id INTEGER, articul INTEGER, num INTEGER)""")
            con.commit()
            data = cursor.fetchone()
            temp = [id, art, num]
            if data is None:
                cursor.execute('INSERT INTO orders VALUES(?,?,?);', temp)
                con.commit()

    except sqlite3.Error as error:
        logger.info("Ошибка при работе с SQLite: {}".format(error))


def del_orders(id: int):
    """Удаление заказа по айди пользователя"""
    try:
        con = sqlite3.connect(r'C:\Users\sklad\base\BD\users.bd')
        with con:
            cursor = con.cursor()

            sql_select_query = """select * from orders where id = ?"""
            cursor.execute(sql_select_query, (id,))
            cursor.execute('DELETE FROM orders WHERE id={}'.format(id))

    except sqlite3.Error as error:
        logger.info("Ошибка при работе с SQLite: {}".format(error))


def mail(message):
    my_list = []
    orders_art = get_bd_info(message.from_user.id)
    for item in orders_art:
        places_dict = search_articul_order(str(item[0]), '012_825')
        my_list.append('⚠️Артикул: {} Кол-во: {}\n{}\n'.format(item[0], item[1], places_dict['name']))
        for i in places_dict['answer']:
            my_list.append('✅ {}\n'.format(i))
    result = '\n'.join(my_list)
    return result
