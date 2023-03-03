import csv
import os

import pandas as pd
from loguru import logger

from data.config import path


def creat_pst():
    groups_list = ['11', '20', '21', '22', '23', '28', '35']
    mini_group = ['Напольные', 'Костюмные', 'Кресла груши', 'Настенные']
    result_for_zero = dict()
    temp_list = []
    for item in groups_list:
        with open('{}/files/file_012_825.csv'.format(path), newline='', encoding='utf-8') as csvfile:
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
    name_dir = '{}/files/pst'.format(path)
    try:
        for f in os.listdir(name_dir):
            os.remove(os.path.join(name_dir, f))
    except:
        pass
    for item in groups_list:
        with open('{}/files/result_{}.csv'.format(path, item), 'w', encoding='utf-8') as file:
            file.write("Код номенклатуры,"
                       "Местоположение,"
                       "Доступно\n")
            for i in data[item]:
                file.write('{}\n'.format(','.join(i)))
        with pd.ExcelWriter('{}/files/pst/pst_{}.xlsx'.format(path, item), engine='xlsxwriter') as writer:
            df = pd.read_csv('{}/files/result_{}.csv'.format(path, item), encoding='utf-8')
            print(df)
            df.to_excel(writer, header=True, index=False, na_rep='')


if __name__ == '__main__':
    save_exsel_pst(creat_pst())
