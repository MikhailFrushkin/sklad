import csv

import pandas as pd
from loguru import logger

from data.config import path
from loader import bot


def dowload(sklad: str):
    if sklad == 'Мин.витрина':
        try:
            excel_data_df = pd.read_excel('{}/utils/file_Мин.витрина.xls'.format(path),
                                          sheet_name='Сток меньше мин витрины',
                                          usecols=['TG',
                                                   'SKU',
                                                   'Name',
                                                   'masterbox qty',
                                                   'box sku qty',
                                                   'showcase min',
                                                   'stock',
                                                   'stock V sale',
                                                   'stock Store',
                                                   'stock Show Room'])
            excel_data_df.to_csv('{}/utils/ctocks.csv'.format(path))
            return True
        except Exception as ex:
            logger.debug(ex)

    else:
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
            return True
        except Exception as ex:
            logger.debug(ex)


def place(message: str, sklad: str) -> list[str]:
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
                        .format(row['Код \nноменклатуры'], row['Описание товара'],
                                0 if row['Доступно'] == '' else row['Доступно'],
                                0 if row['Зарезерви\nровано'] == '' else row[
                                    'Зарезерви\nровано']) \
                        .replace('.0', '')
                    answer.append(line)

        return answer if len(answer) != 0 else 'Ячейка пуста'
    except Exception as ex:
        logger.debug(ex)


def place_dost(message: str, sklad: str) -> list[str]:
    try:
        with open('{}/utils/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            answer = []
            for row in reader:
                if row['Местоположение'].startswith(message) and row['Доступно'] != '':
                    line = '🔄Необходимо убрать с ячейки {}' \
                           '\n{} - {}' \
                           '\nДоступно: {}\n' \
                        .format(row['Местоположение'], row['Код \nноменклатуры'], row['Описание товара'],
                                row['Доступно']) \
                        .replace('.0', '')
                    answer.append(line)
        if len(answer) == 0:
            return ['❌В ячейках нет отказанного товара']
        return answer
    except Exception as ex:
        logger.debug(ex)


def search_articul(art: str, sklad: str) -> list[str]:
    with open('{}/utils/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        answer = []
        for row in reader:
            if row['Код \nноменклатуры'] == art:
                line = '✅{} - {}\n' \
                       '---------------------------------' \
                       '\nДоступно: {} Резерв: {}'.format(row['Местоположение'], row['Описание товара'],
                                                          0 if row['Доступно'] == '' else row['Доступно'],
                                                          0 if row['Зарезерви\nровано'] == '' else row[
                                                              'Зарезерви\nровано']) \
                    .replace('.0', '')
                answer.append(line)
    return answer


def search_name(name: str) -> list[str]:
    with open('{}/utils/file_012_825.csv'.format(path), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        answer = []
        for row in reader:
            if not row['Местоположение'].startswith('012_825-Dost') \
                    and not row['Местоположение'].startswith('012_825-01') \
                    and not row['Местоположение'].startswith('012_825-OX'):
                if name in row['Описание товара'].lower():
                    line = '✅{} - {} Доступно: {}\n' \
                           '{}'.format(row['Местоположение'], row['Код \nноменклатуры'],
                                       0 if row['Доступно'] == '' else row['Доступно'], row['Описание товара']) \
                        .replace('.0', '')
                    answer.append(line)
    return answer


def search_articul_order(art: str, sklad: str) -> list:
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


def search_all_sklad(art: str, sklad: str) -> list[str]:
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


def search_art_name(art: str) -> str:
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
