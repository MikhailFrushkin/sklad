import time

import pandas
from loguru import logger


def main():
    start_time = time.time()

    excel_data_df = pandas.read_excel('Книга1.xlsx', sheet_name='Лист1',
                                      usecols=['Склад',
                                               'Местоположение',
                                               'Код \nноменклатуры',
                                               'Описание товара',
                                               'Доступно',
                                               'Зарезерви\nровано'])
    excel_data_df.to_csv('C:/Users/sklad/all_requests/file.csv')
    logger.info("--- время выполнения функции - {}s seconds ---".format(time.time() - start_time))


if __name__ == '__main__':
    main()