import csv
import json

import pandas as pd
from loguru import logger

from data.config import path


def get_groups():
    try:
        with open('{}/utils/ctocks.csv'.format(path), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            groups_list = sorted(set([(row['TG'][:2], row['TG'][4:].title()) for row in reader]))
            return groups_list
    except Exception as ex:
        logger.debug(ex)


def get_low_stocks_art(group):
    art_groups = []
    with open('{}/utils/ctocks.csv'.format(path), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['TG'][:2] == group and (int(row['stock V sale']) / int(row['showcase min'])) < 0.65:
                art_groups.append((row['SKU'],
                                   row['Name'],
                                   row['showcase min'],
                                   row['stock V sale'],
                                   row['stock Show Room']))
    return art_groups


def _union_result(row: dict, result: dict) -> dict:
    try:
        result[row['Код \nноменклатуры']] += int(row['Доступно'].
                                                 replace('.0', ''))
    except KeyError:
        result[row['Код \nноменклатуры']] = int(row['Доступно'].
                                                replace('.0', ''))
    return result


def union_art2(group: str):
    with open('{}/utils/file_012_825.csv'.format(path), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        result = dict()
        for row in reader:
            if row['ТГ'] == group:
                if row['Доступно'].replace('.0', '').isdigit() and not row['Местоположение'].startswith(
                        '012_825-OX') \
                        and not row['Местоположение'].startswith('012_825-Dost'):
                    result = _union_result(row, result)
    return result


def finish(group):
    low_stock = get_low_stocks_art(group)
    stock_sklad = union_art2(group)
    result = []
    result_for_file = []
    for item in low_stock:
        if item[0] in stock_sklad.keys():
            order = (int(item[2]) - int(item[3])) \
                if (int(item[2]) - int(item[3])) < stock_sklad[item[0]] \
                else stock_sklad[item[0]]
            result.append(('⛳{art} {name}\nМин.сток:{min} К заказу:{order}'.format(
                art=item[0],
                name=item[1],
                min=item[2],
                order=order
            )))

            result_for_file.append([item[0], item[1].replace("", ''),
                                    item[2], item[3], item[4], str(order)])
    return result, result_for_file


def save_exsel_min(group):
    result = finish(group)[1]
    with open('result_min_vitrina{}.csv'.format(group), 'w', newline='', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["Артикул",
                              "Номенкулатура",
                              "Мин.сток",
                              "Запас в зале",
                              "На руме",
                              "К заказу"])
        for i in result:
            file_writer.writerow(i)
    try:
        df = pd.read_csv('result_min_vitrina{}.csv'.format(group), delimiter=',', encoding='utf-8')
        writer = pd.ExcelWriter('{}/files/min_vitrina_{}.xlsx'.format(path, group))
        df.style.apply(_align_left, axis=0).to_excel(writer, sheet_name='Sheet1', index=False, na_rep='NaN')
        writer.sheets['Sheet1'].set_column(0, 7, 15)
        writer.sheets['Sheet1'].set_column(1, 1, 50)
        writer.save()
    except Exception as ex:
        logger.debug(ex)


def _align_left(x):
    return ['text-align: left' for x in x]


if __name__ == '__main__':
    save_exsel_min('28')
