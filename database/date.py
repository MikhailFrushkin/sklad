import csv
import datetime
import os

from loguru import logger

from database.connect_DB import *
import peewee
from peewee import *

from data.config import path


class BaseModel(Model):
    class Meta:
        database = dbdate


class Vsl(BaseModel):
    id = PrimaryKeyField(null=False)
    vendor_code = IntegerField()
    place = CharField(max_length=25)
    name = TextField()
    group = CharField(max_length=5)
    num_old = IntegerField(default=0)
    num_new = IntegerField(default=0)

    class META:
        database = dbdate
        db_table = 'Vsl'
        order_by = ['vendor_code']


class DateBase(BaseModel):
    id = PrimaryKeyField(null=False)
    date_V_Sales_old = DateField(default=datetime.date.today)
    date_V_Sales_new = DateField(default=datetime.date.today)
    date_011_825 = DateField(default=datetime.date.today)
    date_012_825 = DateField(default=datetime.date.today)
    date_A11_825 = DateField(default=datetime.date.today)
    date_RDiff = DateField(default=datetime.date.today)
    date_RDiff_old = DateField(default=datetime.date.today)

    class META:
        database = dbdate
        db_table = 'datebase'
