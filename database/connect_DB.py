import peewee

from data.config import path

user = 'root'
password = 'root'
db_name = 'Product'

dbhandle = peewee.SqliteDatabase('{}/database/mydatabase.db'.format(path))
