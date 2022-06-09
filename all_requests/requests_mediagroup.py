import datetime
import json
import re

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By

from data.config import path_chrom_driver, path


def timer(func):
    def wrapper(*args, **kwargs):
        logger.info('Оборачиваемая функция: {}'.format(func.__name__))
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        logger.info(end - start)
        return result
    return wrapper


@timer
def get_info_only_image(art: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')

    driver = webdriver.Chrome(
        executable_path=f'{path_chrom_driver}',
        options=options
    )
    url = 'https://hoff.ru/vue/search/?fromSearch=direct&search={}&redirect_search=true'.format(art)
    driver.get(url)
    url2 = _get_second_url(driver.page_source)
    driver.get(url2)
    driver.implicitly_wait(10)
    try:
        urls = _get_one_image(driver)
        data = {
            'url_imgs': urls
        }
        with open("{}/base/json/{}_photo.json".format(path, art), "w", encoding='utf-8') as write_file:
            json.dump(data, write_file, indent=4, ensure_ascii=False)
        driver.quit()

        return data

    except Exception as ex:
        logger.debug(ex)


@timer
def get_info(art: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')

    driver = webdriver.Chrome(
        executable_path=f'{path_chrom_driver}',
        options=options
    )
    url = 'https://hoff.ru/vue/search/?fromSearch=direct&search={}&redirect_search=true'.format(art)
    driver.get(url)
    url2 = _get_second_url(driver.page_source)
    driver.get(url2)
    driver.implicitly_wait(10)
    try:
        name = _get_name(driver)
        # params = _get_param(driver)
        urls = _get_image(driver)
        price = _get_price(driver)
        data = {
            'name': name,
            # 'params': params,
            'price': price,
            'url_imgs': urls
        }
        with open("{}/base/json/{}.json".format(path, art), "w", encoding='utf-8') as write_file:
            json.dump(data, write_file, indent=4, ensure_ascii=False)
        driver.quit()
        return data

    except Exception as ex:
        logger.debug(ex)


@timer
def _get_second_url(text) -> str:
    pattern = r'(?<=\\).+?["]'
    result = re.search(pattern, text)
    url_page1 = 'https://hoff.ru' + result[0][:-1]
    url = url_page1.replace('\\', '')

    logger.info('URL товара - {}'.format(url))
    return url


@timer
def _get_name(driver):
    name = driver.find_element(
        by=By.CLASS_NAME,
        value='page-title')
    name_item = name.text
    logger.info('Имя -{}'.format(name_item))
    return name_item


@timer
def _get_params(driver) -> list[str]:
    list_param = []
    params = driver.find_elements(
        by=By.CLASS_NAME,
        value='product-params-item')
    for i_item in params:
        list_param.append(i_item.text)
    logger.info('Список параметров -{}'.format(list_param))
    return list_param


@timer
def _get_image(driver) -> list[str]:
    img = driver.find_elements(
        by=By.CLASS_NAME,
        value='preview')
    url_list = []
    for item in range(len(img)):
        if item != 5:
            src = img[item].get_attribute('style')
            print(src)
            pattern = r'(?<=").+?[g]'
            url_img = re.search(pattern, src)
            url_list.append(url_img[0])
        else:
            break
    logger.info(url_list)
    return url_list


@timer
def _get_one_image(driver) -> list[str]:
    img = driver.find_elements(
        by=By.CLASS_NAME,
        value='preview')
    url_list = []
    for item in range(len(img)):
        if item != 5:
            src = img[item].get_attribute('style')
            print(src)
            pattern = r'(?<=").+?[g]'
            url_img = re.search(pattern, src)
            url_list.append(url_img[0])
        else:
            break
    logger.info(url_list)
    return url_list


@timer
def _get_price(driver) -> str:
    try:
        price = driver.find_element(
            by=By.CLASS_NAME,
            value='product-price-benefits').find_element(by=By.CLASS_NAME,
                                                         value='product-price')
        price = price.text
        logger.info([price])
    except Exception as ex:
        logger.debug(ex)
        price = 'Нет цены на сайте, либо товар закончился'
    return price


if __name__ == '__main__':
    get_info('80357183')
