import datetime
import json
import re
import time

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By

from data.config import path_chrom_driver, path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        logger.info('Время выполнения функции {} - {}'.format(func.__name__, end - start))
        return result

    return wrapper


@timer
def get_actions():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--headless')

    driver = webdriver.Chrome(
        executable_path=f'{path_chrom_driver}',
        options=options
    )
    url = 'https://hoff.ru/actions/'
    driver.get(url)
    driver.implicitly_wait(10)
    try:
        data = _get_category(driver)
        _get_name_category(data)
        # with open("{}/base/Actions/category.json".format(path), "w", encoding='utf-8') as write_file:
        #     json.dump(data, write_file, indent=4, ensure_ascii=False)
        driver.quit()

        return data
    except Exception as ex:
        logger.debug(ex)


@timer
def _get_category(driver):
    category = driver.find_element(
        by=By.CLASS_NAME,
        value='products')
    return category


@timer
def _get_name_category(driver):
    wait = WebDriverWait(driver, 10)
    try:
        button = driver.find_element(by=By.XPATH,
                                     value="//*[@id='hoff-app']/section/section/div[2]/div[2]/div[1]/button").click()
    except Exception as ex:
        logger.debug(ex)
    time.sleep(1)
    try:
        name_list = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "products-item"))
        )
        names = []
        for item in name_list:
            names.append(item.find_element(by=By.CSS_SELECTOR,
                                           value='#hoff-app > section > section > div.discount > div.discount-container > div.products-on-sale > div.products > div:nth-child(1)').get_attribute('href'))
        print(names)
    except Exception as ex:
        logger.debug(ex)


if __name__ == '__main__':
    get_actions()
