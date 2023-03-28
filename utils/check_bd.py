from loguru import logger

from database.connect_DB import dbhandle
from database.users import Users


def check(message):
    user = Users.get(Users.id_tg == message.from_user.id)
    if user.black_status == True:
        return 3
    if user:
        return True
