import csv
import os

from loguru import logger

from database.connect_DB import *
import peewee
from peewee import *

from data.config import path


class BaseModel(Model):
    class Meta:
        database = dbhandle


class Product(BaseModel):
    id = PrimaryKeyField(null=False)
    vendor_code = CharField(max_length=8)
    place = CharField(max_length=25)
    name = TextField()
    group = CharField(max_length=10)
    minigroup_name = CharField()
    status = CharField(default='Не проверен')
    user_id = CharField(max_length=20, default='')
    updated_at = DateTimeField(default=0)

    @staticmethod
    def list():
        query = Product.select()
        for row in query:
            print(row.id, row.vendor_code, row.name, row.group, row.minigroup_name, row.status)
        return Product.select()

    @staticmethod
    def update_bot():
        myfile = '{}/database/mydatabase.db'.format(path)
        if os.path.isfile(myfile):
            dbhandle.connect()
            try:
                with open('{}/utils/file_V_Sales.csv'.format(path), newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row['Физические \nзапасы'] == '1' and row['Местоположение'] == 'V-Sales_825':
                            place = row['Местоположение']
                            art = row['Код \nноменклатуры']
                            name = row['Описание товара']
                            group = row['ТГ']
                            minigroup_name = row['Краткое наименование']

                            try:
                                temp = Product.get(Product.vendor_code == int(art))
                            except Exception as ex:
                                temp = Product.create(vendor_code=art, name=name, group=group,
                                                      place=place, minigroup_name=minigroup_name)
                                temp.save()
                                logger.debug('новый арт добавлен {}'.format(temp))
                arts_bd = [i.vendor_code for i in Product.select()]

                with open('{}/utils/file_V_Sales.csv'.format(path), newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    new_art_exsel = []
                    for row in reader:
                        if row['Физические \nзапасы'] == '1' and row['Местоположение'] == 'V-Sales_825':
                            new_art_exsel.append(int(row['Код \nноменклатуры']))
                    for item in arts_bd:
                        if item not in new_art_exsel:
                            try:
                                obj = Product.get(Product.vendor_code == item)
                                obj.delete_instance()
                                logger.info('арт удален {}'.format(item))
                            except Exception as ex:
                                logger.debug(ex)

                logger.info('База единичек обновлена')
            except peewee.InternalError as px:
                print(str(px))
            finally:
                dbhandle.close()
        else:
            dbhandle.connect()
            Product.create_table()
            try:

                with open('{}/utils/file_V_Sales.csv'.format(path), newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row['Физические \nзапасы'] == '1' and row['Местоположение'] == 'V-Sales_825':
                            place = row['Местоположение']
                            art = row['Код \nноменклатуры']
                            name = row['Описание товара']
                            group = row['ТГ']
                            minigroup_name = row['Краткое наименование']
                            temp = Product.create(vendor_code=art, name=name, group=group,
                                                  place=place, minigroup_name=minigroup_name)
                            temp.save()
                logger.info('База единичек создана')
                arts_bd = [i.vendor_code for i in Product.select()]
            except peewee.InternalError as px:
                print(str(px))
            finally:
                dbhandle.close()
        return len(arts_bd)

    class META:
        database = dbhandle
        db_table = 'Product'
        order_by = ['vendor_code']
