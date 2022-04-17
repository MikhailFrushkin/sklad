import csv
import time
import pandas as pd

from loguru import logger

import io
import requests


def place(message):
    start_time = time.time()

    # excel_data_df = pandas.read_excel('Книга1.xlsx', sheet_name='Лист1',
    #                                   usecols=['Склад',
    #                                            'Местоположение',
    #                                            'Код \nноменклатуры',
    #                                            'Описание товара',
    #                                            'Доступно',
    #                                            'Зарезерви\nровано'])
    # excel_data_df.to_csv('C:/Users/sklad/utils/file.csv')
    # logger.info("--- время выполнения функции - {}s seconds ---".format(time.time() - start_time))

    with open('C:/Users/sklad/utils/file.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        answer = []
        for row in reader:
            if row['Местоположение'] == message:
                line = '{} - {}\n' \
                       '---------------------------------' \
                       '\nДоступно: {} Резерв: {}'.format(
                    row['Код \nноменклатуры'],
                    row['Описание товара'],
                    0 if row['Доступно'] == '' else row['Доступно'],
                    0 if row['Зарезерви\nровано'] == '' else row[
                        'Зарезерви\nровано']) \
                    .replace('.0', '')
                answer.append(line)
    return answer


def search_articul(art):
    with open('C:/Users/sklad/utils/file.csv', newline='', encoding='utf-8') as csvfile:
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
