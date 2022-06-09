import csv

import pandas as pd
from loguru import logger

from data.config import path


def dowload(sklad):
    try:
        excel_data_df = pd.read_excel('{}/utils/file_{}.xls'.format(path, sklad), sheet_name='Лист1',
                                      usecols=['Склад',
                                               'Местоположение',
                                               'Код \nноменклатуры',
                                               'Краткое наименование',
                                               'Описание товара',
                                               'Доступно',
                                               'Зарезерви\nровано',
                                               'ТГ'])
        excel_data_df.to_csv('{}/utils/file_{}.csv'.format(path, sklad))
    except Exception as ex:
        logger.debug(ex)


def place(message, sklad):
    try:
        with open('{}/utils/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            answer = []
            for row in reader:
                if row['Местоположение'] == message:
                    line = '{} - {}' \
                           '\n---------------------------------' \
                           '\nДоступно: {} Резерв: {}' \
                           '\n---------------------------------' \
                        .format(
                        row['Код \nноменклатуры'],
                        row['Описание товара'],
                        0 if row['Доступно'] == '' else row['Доступно'],
                        0 if row['Зарезерви\nровано'] == '' else row[
                            'Зарезерви\nровано']) \
                        .replace('.0', '')
                    answer.append(line)
        return answer
    except Exception as ex:
        logger.debug(ex)


def place_dost(message, sklad):
    try:
        with open('{}/utils/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            answer = []
            for row in reader:
                if row['Местоположение'].startswith(message) and row['Доступно'] != '':
                    line = '🔄Необходимо убрать с ячейки {}' \
                           '\n{} - {}' \
                           '\nДоступно: {}\n' \
                        .format(
                        row['Местоположение'],
                        row['Код \nноменклатуры'],
                        row['Описание товара'],
                        row['Доступно']) \
                        .replace('.0', '')
                    answer.append(line)
        if len(answer) == 0:
            return ['❌В ячейках нет отказанного товара']
        return answer
    except Exception as ex:
        logger.debug(ex)


def search_articul(art, sklad):
    with open('{}/utils/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        answer = []
        for row in reader:
            if row['Код \nноменклатуры'] == art:
                line = '✅{} - {}\n' \
                       '---------------------------------' \
                       '\nДоступно: {} Резерв: {}'.format(
                    row['Местоположение'],
                    row['Описание товара'],
                    0 if row['Доступно'] == '' else row['Доступно'],
                    0 if row['Зарезерви\nровано'] == '' else row[
                        'Зарезерви\nровано']) \
                    .replace('.0', '')
                answer.append(line)
    return answer


def search_articul_order(art, sklad):
    try:
        with open('{}/utils/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            art_list = []
            art_dict = {
                'Код': '',
                'Местоположение': '',
                'Описание товара': '',
                'Доступно': ''
            }
            for row in reader:
                if row['Код \nноменклатуры'] == art:
                    art_dict['Код'] = art
                    art_dict['Местоположение'] = row['Местоположение']
                    art_dict['Описание товара'] = row['Описание товара']
                    art_dict['Доступно'] = row['Доступно'].replace('.0', '')
                    art_list.append(art_dict)
                    art_dict = {
                        'Код': '',
                        'Местоположение': '',
                        'Описание товара': '',
                        'Доступно': ''
                    }
        if len(art_list) > 0:
            return art_list
        else:
            raise Exception
    except Exception as ex:
        logger.debug('❌Артикул не найден на складе {}'.format(ex))


def search_all_sklad(art, sklad):
    with open('{}/utils/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        answer = []
        for row in reader:
            if row['Код \nноменклатуры'] == art:
                line = '✅{} - Доступно: {} Резерв: {}'.format(
                    row['Местоположение'],
                    0 if row['Доступно'] == '' else row['Доступно'],
                    0 if row['Зарезерви\nровано'] == '' else row[
                        'Зарезерви\nровано']) \
                    .replace('.0', '')
                answer.append(line)
    return answer


def search_art_name(art):
    line = 'Нет товара в наличии'
    sklad_list = ['011_825', '012_825', 'A11_825', 'V_Sales', 'RDiff']
    for i in sklad_list:
        with open('{}/utils/file_{}.csv'.format(path, i), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Код \nноменклатуры'] == art:
                    line = '{}'.format(row['Описание товара'])
    return line


if __name__ == '__main__':
    print(search_art_name('80419935'))
