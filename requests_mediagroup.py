import re
import time

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_photo(art):
    url = 'https://hoff.ru/vue/search/?fromSearch=direct&search={}&redirect_search=true'.format(art)

    try:
        start_time = time.time()

        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chromeOptions)

        driver.get(url)
        text = driver.page_source
        pattern = r'(?<=\\).+?["]'
        result = re.search(pattern, text)
        url_page1 = 'https://hoff.ru' + result[0][:-1]
        url = url_page1.replace('\\', '')

        logger.info('URL товара - {}'.format(url))

        driver.get(url)
        time.sleep(3)
        name = driver.find_element(
                by=By.CLASS_NAME,
                value='page-title')
        name_item = name.text

        try:
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
            logger.info(url_list)
            logger.info("--- время выполнения функции - {}s seconds ---".format(time.time() - start_time))
            return url_list, name_item
        except Exception as ex:
            print(ex)
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    get_photo('80368069')
