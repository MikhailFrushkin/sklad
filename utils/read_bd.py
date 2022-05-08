import sqlite3


def get_bd_info(id):
    """чтение бд"""
    try:
        sqlite_connection = sqlite3.connect(r'C:\Users\sklad\base\BD\users.bd')
        cursor = sqlite_connection.cursor()

        sql_select_query = """select * from login_id where id = ?"""
        cursor.execute(sql_select_query, (id,))
        records = cursor.fetchall()
        data = dict()
        for row in records:
            data["ID:"] = row[0]
            data["Имя:"] = row[1]
            data["Дата регистрации:"] = row[2]
            data["БЮ:"] = row[3]
            data["Заказ"] = row[4]
        return data
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


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
        print("Ошибка при работе с SQLite", error)


def del_order(id: int):
    """Создание строк с айди, артикул и количество для заказа"""
    try:
        con = sqlite3.connect(r'C:\Users\sklad\base\BD\users.bd')
        with con:
            cursor = con.cursor()

            sql_select_query = """select * from orders where id = ?"""
            cursor.execute(sql_select_query, (id,))
            cursor.execute('DELETE FROM orders WHERE id={}'.format(id))

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

