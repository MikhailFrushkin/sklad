import sqlite3

from loguru import logger

from data.config import path


def check(message):
    try:
        connect = sqlite3.connect('{}/base/BD/users.bd'.format(path))
        cursor = connect.cursor()

        # cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(id INTEGER, name TEXT, date REAL)""")
        # connect.commit()
        cursor.execute('SELECT Black_status FROM login_id WHERE id = {}'.format(message.from_user.id))
        data_black = cursor.fetchone()
        if data_black[0] == 0:
            cursor.execute('SELECT id FROM login_id WHERE id = {}'.format(message.from_user.id))
            data = cursor.fetchone()
            if data is None:
                return False
            return True
        else:
            return 3
    except Exception as ex:
        logger.debug(ex)
