from base64 import b64decode
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_photo(art):
    key = 'hoff {}'.format(art)
    url = 'https://www.google.ru/search?q={}&newwindow=1&espv=2&source=lnms&tbm=isch&sa=X'.format(key)

    try:
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.get(url)
        driver.find_element(by=By.XPATH, value='//img[starts-with(@src, "data:image/jpeg;base64,")]').click()
        time.sleep(2)
        img = driver.find_element(
            by=By.XPATH,
            value='//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img')

        src = img.get_attribute('src')
        print(src)
        if 'data:image/jpeg;base64,' in src:
            src = src.split('data:image/jpeg;base64,')[1]
            print(src)
        return src

    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    get_photo('80418856')
