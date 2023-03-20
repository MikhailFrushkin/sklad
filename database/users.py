import datetime

from peewee import *

from database.connect_DB import *


class BaseModel(Model):
    class Meta:
        database = dbhandle


class Keyboard(BaseModel):
    id = PrimaryKeyField(null=False)
    vsales = BooleanField(default=True)
    ex_sklad = BooleanField(default=True)
    qr_cell = BooleanField(default=True)
    text_qr = BooleanField(default=True)
    content = BooleanField(default=True)
    search = BooleanField(default=True)
    check = BooleanField(default=True)
    buy = BooleanField(default=True)
    check_one = BooleanField(default=True)
    stock = BooleanField(default=True)
    info = BooleanField(default=True)
    tel = BooleanField(default=True)

    class META:
        database = dbhandle
        db_table = 'Keyboard'
        order_by = ['id']


class Users(BaseModel):
    id = PrimaryKeyField()
    id_tg = IntegerField()
    name = CharField(max_length=150)
    created_at = DateTimeField(default=datetime.datetime.now)
    shop = CharField(default='')
    black_status = BooleanField(default=False)
    keyboard = ForeignKeyField(Keyboard, backref='keyboard', on_delete='cascade', on_update='cascade')

    class META:
        database = dbhandle
        db_table = 'Users'
        order_by = ['created_at']
        primary_key = CompositeKey('keyboard')


class Operations(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, on_delete='cascade', on_update='cascade')
    date = DateTimeField(default=datetime.datetime.now)
    operation = CharField(max_length=50)
    comment = CharField(max_length=50)

    class META:
        database = dbhandle
        db_table = 'Operations'
        order_by = ['date']
        primary_key = CompositeKey('user')
