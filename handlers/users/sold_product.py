import csv
import os

from loguru import logger
from database.date import *
import pandas as pd
from database.connect_DB import *
import peewee
from peewee import *

from data.config import path


def read_base_vsl():
    data_art = {}
    try:
        with open('{}/files/file_old_V_Sales.csv'.format(path), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_art[row['Код \nноменклатуры']] = \
                    {'Описание товара': row['Описание товара'],
                     'ТГ': row['ТГ'],
                     'Доступно было': 0 if row['Доступно'] == '' else int(row['Доступно'].replace('.0', ''))}

    except Exception as ex:
        logger.debug(ex)

    try:
        with open('{}/files/file_V_Sales.csv'.format(path), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Код \nноменклатуры'] in data_art.keys():
                    data_art[row['Код \nноменклатуры']]['Доступно стало'] = 0 if row['Доступно'] == '' \
                        else int(row['Доступно'].replace('.0', ''))
                    data_art[row['Код \nноменклатуры']]['Дельта'] = \
                        data_art[row['Код \nноменклатуры']]['Доступно стало'] - data_art[row['Код \nноменклатуры']][
                            'Доступно было']
    except Exception as ex:
        logger.debug(ex)

    result_dict = {}
    for key, value in data_art.items():
        try:
            if value['Дельта'] < 0:
                result_dict[key] = {
                    'Артикул': key,
                    'Описание товара': value['Описание товара'],
                    'ТГ': value['ТГ'],
                    'Проданно': -value['Дельта'],
                    'Остаток VSL': value['Доступно стало']
                }
        except Exception as ex:
            pass

    union_atr = dict()
    output = list()
    try:
        with open('{}/files/file_012_825.csv'.format(path), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not row['Местоположение'].startswith('012_825-Dost') \
                        and not row['Местоположение'].startswith('012_825-01') \
                        and not row['Местоположение'].startswith('012_825-OX'):
                    union_atr = _union_result_for_zero(row, union_atr)
            for key, value in union_atr.items():
                if key[0] in result_dict.keys() and value > 0:
                    result_dict[key[0]]['На складе'] = value
    except Exception as ex:
        logger.debug(ex)
    for key, value in result_dict.items():
        if len(value) == 6:
            output.append([i for i in value.values()])
    result_for_exsel(output)


def _union_result_for_zero(row: dict, union_atr) -> dict:
    try:
        union_atr[(row['Код \nноменклатуры'], row['Описание товара'])] += 0 if row['Доступно'] == '' else int(
            row['Доступно'].replace('.0', ''))
    except KeyError:
        union_atr[(row['Код \nноменклатуры'], row['Описание товара'])] = 0 if row['Доступно'] == '' else int(
            row['Доступно'].
            replace('.0', ''))
    return union_atr


def result_for_exsel(output):
    list_list = []
    for i in output:
        list_list.append(i[2])
    list_group = (sorted(list(set(list_list))))
    try:
        writer = pd.ExcelWriter('{}/files/sold.xlsx'.format(path))
        for group in list_group:
            data = {
                'Артикул': [],
                'Описание товара': [],
                'ТГ': [],
                'Проданно': [],
                'Остаток VSL': [],
                'На складе': []}
            for i in output:
                if group == i[2]:
                    data['Артикул'].append(i[0])
                    data['Описание товара'].append(i[1])
                    data['ТГ'].append(i[2])
                    data['Проданно'].append(i[3])
                    data['Остаток VSL'].append(i[4])
                    data['На складе'].append(i[5])
            df_marks = pd.DataFrame(data)
            sorted_df = df_marks.sort_values(by='Проданно', ascending=False)
            sorted_df.to_excel(writer, sheet_name='{}'.format(group), index=False, na_rep='NaN')

            workbook = writer.book
            worksheet = writer.sheets['{}'.format(group)]

            cell_format2 = workbook.add_format()
            cell_format2.set_align('left')

            cell_format3 = workbook.add_format()
            cell_format3.set_align('center')

            worksheet.set_column('A:A', 18, cell_format2)
            worksheet.set_column('B:B', 80, cell_format2)
            worksheet.set_column('C:F', 12, cell_format3)
        writer.close()
    except Exception as ex:
        logger.debug(ex)


if __name__ == '__main__':
    read_base_vsl()
