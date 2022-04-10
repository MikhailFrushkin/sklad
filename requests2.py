import re
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
        print('URL товара - ', url)

        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(3)
        try:
            img = driver.find_element(
                by=By.XPATH,
                value='//*[@id="hoff-app"]/section/section/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/a/img')
            src = img.get_attribute('src')
            print('первый', src)
            return src
        except Exception as ex:
            print(ex)
        try:
            img = driver.find_element(
                by=By.XPATH,
                value='//*[@id="hoff-app"]/section/section/div[2]/div/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/a/img')
            src = img.get_attribute('src')
            print('второй', src)
            return src
        except Exception as ex:
            print(ex)

    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    get_photo('80322475')
