import sqlite3

from loguru import logger


def check(id):
    try:
        connect = sqlite3.connect('C:/Users/sklad/base/BD/users.bd')
        cursor = connect.cursor()

        # cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(id INTEGER, name TEXT, date REAL)""")
        # connect.commit()

        cursor.execute('SELECT id FROM login_id WHERE id = {}'.format(id))
        data = cursor.fetchone()
        if data is None:
            # date = datetime.datetime.now()
            # user_id = [message.chat.id, message.from_user.first_name, date]
            # cursor.execute('INSERT INTO login_id VALUES(?,?,?);', user_id)
            # connect.commit()
            return False
        return True
    except Exception as ex:
        logger.debug(ex)