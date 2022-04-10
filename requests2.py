import re

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_photo(art):
    url = 'https://hoff.ru/vue/search/?fromSearch=direct&search={}&redirect_search=true'.format(art)

    try:
        driver = webdriver.Chrome()
        driver.get(url)
        text = driver.page_source
        pattern = r'(?<=\\).+?["]'
        result = re.search(pattern, text)
        url_page1 = 'https://hoff.ru' + result[0][:-1]
        url = url_page1.replace('\\', '')

        logger.info('URL товара - {}'.format(url))

        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(3)
        try:
            img = driver.find_element(
                by=By.CLASS_NAME,
                value='preview')
            src = img.get_attribute('style')
            pattern = r'(?<=").+?[g]'
            url_img = re.search(pattern, src)

            logger.info('URL картинки - {}'.format(url_img[0]))
            return url_img[0]
        except Exception as ex:
            print(ex)
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    get_photo('80322475')
