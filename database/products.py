import csv
from database.connect_DB import *
import peewee
from peewee import *

from data.config import path


class BaseModel(Model):
    class Meta:
        database = dbhandle


class Product(BaseModel):
    id = PrimaryKeyField(null=False)
    vendor_code = CharField(max_length=10)
    name = TextField()
    group = CharField(max_length=10)
    status = CharField(default='Не проверен')
    property = CharField(max_length=20, default='')
    updated_at = DateTimeField(default=0)

    @staticmethod
    def list():
        query = Product.select()
        for row in query:
            print(row.id, row.vendor_code, row.name, row.group, row.status)
        return Product.select()

    class META:
        database = dbhandle
        db_table = 'Product'


if __name__ == '__main__':
    dbhandle.connect()
    Product.list()
    # Product.create_table()
    # try:
    #     with open('{}/utils/file_V_Sales.csv'.format(path), newline='', encoding='utf-8') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             if row['Физические \nзапасы'] == '1':
    #                 art = row['Код \nноменклатуры']
    #                 name = row['Описание товара']
    #                 group = row['ТГ']
    #                 temp = Product.create(vendor_code=art, name=name, group=group)
    #                 temp.save()
    # except peewee.InternalError as px:
    #     print(str(px))
    # finally:
    #     dbhandle.close()

