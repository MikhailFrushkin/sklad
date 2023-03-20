from loguru import logger

from database.users import Users


def check(message):
    try:
        user = Users.get(Users.id_tg == message.from_user.id)
        if user.black_status == True:
            return 3
        if user:
            return True

    except Exception as ex:
        logger.debug(ex)
