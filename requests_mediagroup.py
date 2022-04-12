import re
import time
import json

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_info(art: str) -> tuple:
    """
    Получение от пользователя артикула, парсим первый сайт для получения урла товара.
    После парсим урл товара, берем нужную инфу, возвращаем ее кортежем.
    :param art: srt
    :return: tuple
    """
    url: str = 'https://hoff.ru/vue/search/?fromSearch=direct&search={}&redirect_search=true'.format(art)
    try:
        start_time = time.time()

        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.minimize_window()
        driver.get(url)
        text = driver.page_source
        pattern = r'(?<=\\).+?["]'
        result = re.search(pattern, text)
        url_page1 = 'https://hoff.ru' + result[0][:-1]
        url = url_page1.replace('\\', '')

        logger.info('URL товара - {}'.format(url))

        driver.get(url)
        time.sleep(3)

        try:
            name = driver.find_element(
                by=By.CLASS_NAME,
                value='page-title')
            name_item = name.text

            list_param = []
            params = driver.find_elements(
                by=By.CLASS_NAME,
                value='product-params-item')
            for i_item in params:
                list_param.append(i_item.text)
            print(list_param)

            img = driver.find_elements(
                by=By.CLASS_NAME,
                value='preview')
            url_list = []
            for item in range(len(img)):
                if not item == 3:
                    src = img[item].get_attribute('style')
                    logger.info(src)
                    pattern = r'(?<=").+?[g]'
                    url_img = re.search(pattern, src)
                    url_list.append(url_img[0])
                    logger.info('URL картинки - {}'.format(url_img[0]))
                else:
                    break
            try:
                price = driver.find_element(
                    by=By.CLASS_NAME,
                    value='product-price-benefits').find_element(by=By.CLASS_NAME,
                                                                 value='product-price')
                price = price.text
            except Exception as ex:
                logger.info('Нет цены', ex)
                price = 'Упс. Нет цены на сайте'
            logger.info(url_list)
            logger.info("--- время выполнения функции - {}s seconds ---".format(time.time() - start_time))

            data = {
                'url_imgs': url_list,
                'name': name_item,
                'params': list_param,
                'price': price
            }
            with open("base/{}.json".format(art), "w", encoding='utf-8') as write_file:
                json.dump(data, write_file, indent=4, ensure_ascii=False)

            return url_list, name_item, list_param, price
        except Exception as ex:
            print(ex)
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    get_info('80368069')
