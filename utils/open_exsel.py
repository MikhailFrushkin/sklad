import openpyxl
import json
import time
import pandas


from loguru import logger


def main():
    start_time = time.time()

    excel_data_df = pandas.read_excel('Книга1.xlsx', sheet_name='Лист1')
    print(set(excel_data_df['Склад'].tolist()))
    print(sorted(set(excel_data_df['Местоположение'].tolist())))

    logger.info("--- время выполнения функции - {}s seconds ---".format(time.time() - start_time))


if __name__ == '__main__':
    main()
