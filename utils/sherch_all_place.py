import csv

import pandas as pd
from loguru import logger

from data.config import path


def creat_pst():
    groups_list = ['11', '20', '21', '22', '23', '28', '35']
    mini_group = ['Напольные', 'Костюмные', 'Кресла груши', 'Настенные']
    result_for_zero = dict()
    temp_list = []
    for item in groups_list:
        with open('{}/utils/file_012_825.csv'.format(path), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if item == '35':
                    if row['ТГ'] == '35' and row['Краткое наименование'] in mini_group:
                        if row['Доступно'].replace('.0', '').isdigit() and not row['Местоположение'].startswith(
                                '012_825-OX') \
                                and not row['Местоположение'].startswith('012_825-Dost'):
                            temp_list.append([row['Код \nноменклатуры'],
                                              row['Местоположение'],
                                              row['Доступно'].replace('.0', '')])
                elif row['ТГ'] == item:
                    temp_list.append([row['Код \nноменклатуры'],
                                      row['Местоположение'],
                                      row['Доступно'].replace('.0', '')])
                else:
                    continue
        result_for_zero[item] = temp_list
        temp_list = []
    return result_for_zero


def save_exsel_pst(data):
    groups_list = ['11', '20', '21', '22', '23', '28', '35']
    for item in groups_list:
        with open('result_{}.csv'.format(item), 'w', encoding='utf-8') as file:
            file.write("Код номенклатуры,"
                       "Местоположение,"
                       "Доступно\n")
            for i in data[item]:
                file.write('{}\n'.format(','.join(i)))
        df = pd.read_csv('result_{}.csv'.format(item), encoding='utf-8')
        df.to_excel('pst_{}.xlsx'.format(item), 'Sheet1', index=False)


if __name__ == '__main__':
    save_exsel_pst(creat_pst())
