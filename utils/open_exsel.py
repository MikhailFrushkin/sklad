import csv

import pandas as pd
from loguru import logger


def dowload(sklad):
    try:
        excel_data_df = pd.read_excel('C:/Users/sklad/file_{}.xls'.format(sklad), sheet_name='Лист1',
                                      usecols=['Склад',
                                               'Местоположение',
                                               'Код \nноменклатуры',
                                               'Описание товара',
                                               'Доступно',
                                               'Зарезерви\nровано'])
        excel_data_df.to_csv('C:/Users/sklad/utils/file_{}.csv'.format(sklad))
    except Exception as ex:
        logger.debug(ex)


def place(message, sklad):
    try:
        print(message, sklad)
        with open('C:/Users/sklad/utils/file_{}.csv'.format(sklad), newline='', encoding='utf-8') as csvfile:
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


def search_articul(art, sklad):
    with open('C:/Users/sklad/utils/file_{}.csv'.format(sklad), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        answer = []
        for row in reader:
            if row['Код \nноменклатуры'] == art:
                line = '{} - {}\n' \
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


if __name__ == '__main__':
    print(search_articul('80419935'))
