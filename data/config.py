from pathlib import Path

from environs import Env

path = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN2')
ADMINS = env.list('ADMINS')
PASSWORD = env.str('PASSWORD')


def hidden():
    with open('{}/files/hidden.txt'.format(path), 'r', encoding='utf-8') as f:
        hidden_mode = f.read()
    if hidden_mode == 'True':
        return True
