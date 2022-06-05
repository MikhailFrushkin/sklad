from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')
PASSWORD = env.str('PASSWORD')

# path = '/Users/sklad'   #сервер
path = 'C:/Users/sklad' #локал

# path_chrom_driver = '/usr/local/bin/chromedriver'
path_chrom_driver = 'C:/Users/sklad/chromedriver.exe'
