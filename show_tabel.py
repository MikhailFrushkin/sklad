import re
import time
import json

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_graf():
    url: str = 'https://time.hoff.ru/timeman/timeman-verme.php?personal_page_id=user_timeman'
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user_agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Mobile Safari/537.36')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(1)

        tabel_input = driver.find_element(by=By.NAME,
                                          value='USER_LOGIN')
        tabel_input.clear()
        tabel_input.send_keys('825078')
        time.sleep(1)

        password_input = driver.find_element(by=By.NAME,
                                          value='USER_PASSWORD')
        password_input.clear()
        password_input.send_keys('trWf@2yNh1')
        time.sleep(1)

        driver.find_element(by=By.CLASS_NAME, value='login-btn').click()
        time.sleep(5)

    except Exception as ex:
        logger.debug(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    get_graf()
