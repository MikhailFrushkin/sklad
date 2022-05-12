import csv
import os
import re
import time
import json

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_info(art: str) -> tuple:
    """
    Скрапим всю нужную инфу с вайта по артикулам которые в наличии на складе 012
    :param art: srt
    :return: tuple
    """

    options = webdriver.ChromeOptions()
    from fake_useragent import UserAgent
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--disable-notifications")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path="C:/Users/sklad/chromedriver.exe",
        options=options
    )
    url: str = 'https://hoff.ru/vue/search/?fromSearch=direct&search={}&redirect_search=true'.format(art)

    driver.get(url)
    time.sleep(1)
    text = driver.page_source
    pattern = r'(?<=\\).+?["]'
    result = re.search(pattern, text)
    url_page1 = 'https://hoff.ru' + result[0][:-1]
    url = url_page1.replace('\\', '')

    logger.info('URL товара - {}'.format(url))
    driver.get(url)
    time.sleep(5)
    try:
        name = driver.find_element(
            by=By.CLASS_NAME,
            value='page-title')
        name_item = name.text

    except Exception as ex:
        name_item = '...'
        logger.debug(ex)

    try:
        list_param = []
        params = driver.find_elements(
            by=By.CLASS_NAME,
            value='product-params-item')
        if params:
            for i_item in params:
                list_param.append(i_item.text)
            logger.info('{} Список параметров -{}'.format(name_item, list_param))
        else:
            raise Exception
    except Exception as ex:
        list_param = []
        logger.debug(ex)

    try:
        img = driver.find_elements(
            by=By.CLASS_NAME,
            value='preview')
        url_list = []
        for item in range(len(img)):
            if not item == 3:
                src = img[item].get_attribute('style')
                pattern = r'(?<=").+?[g]'
                url_img = re.search(pattern, src)
                url_list.append(url_img[0])
            else:
                break
    except Exception as ex:
        logger.debug(ex)

    try:
        price = driver.find_element(
            by=By.CLASS_NAME,
            value='product-price-benefits').find_element(by=By.CLASS_NAME,
                                                         value='product-price')
        price = price.text
    except Exception as ex:
        logger.debug('Нет цены', ex)
        price = 'Упс. Нет цены на сайте'

    data = {
        'url_imgs': url_list,
        'name': name_item,
        'params': list_param,
        'price': price
    }

    with open(r"C:\Users\sklad\base\json\{}.json".format(art), "w", encoding='utf-8') as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)


def all_art():
    """
    Список артикулов из файла
    :return:
    """
    with open('C:/Users/sklad/utils/file_012_825.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        answer = []
        for row in reader:
            line = '{}'.format(row['Код \nноменклатуры'])
            answer.append(line)
    return answer


if __name__ == '__main__':
    art_list = all_art()
    time_start = time.time()
    c = 0
    for item2 in art_list:
        try:
            if os.path.exists(r"C:\Users\sklad\base\json\{}.json".format(item2)):
                logger.info('нашел json ')
                c += 1
            else:
                get_info(item2)
                c += 1
                logger.info('Отсканирован {}\n{} из {}\nПрошло {}'.format(item2, c, len(art_list), time.time() - time_start))
                time.sleep(5)
        except Exception as ex:
            logger.debug(ex)
