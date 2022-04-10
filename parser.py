from base64 import b64decode
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_photo():
    art = 80403089
    key = 'hoff {}'.format(art)
    url = 'https://www.google.ru/search?q={}&newwindow=1&espv=2&source=lnms&tbm=isch&sa=X'.format(key)

    try:
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.get(url)

        img = driver.find_element(by=By.XPATH, value='//img[starts-with(@src, "data:image/jpeg;base64,")]')
        src = img.get_attribute('src')
        src = src.split('data:image/jpeg;base64,')[1]

        img_data = b64decode(src)

        with open('photo\\{}.jpg'.format(art), 'wb') as f:
            f.write(img_data)
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    get_photo()
