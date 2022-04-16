import time

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_graf(message):
    url: str = 'https://time.hoff.ru/timeman/timeman-verme.php?personal_page_id=user_timeman'
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path="C:/Users/sklad/chromedriver.exe",
        options=options
    )
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

        driver.execute_script("""
                (function () {
                    var y = 0;
                    var step = 100;
                    window.scroll(0, 0);
                    function f() {
                        if (y < document.body.scrollHeight) {
                            y += step;
                            window.scroll(0, y);
                            setTimeout(f, 100);
                        } else {
                            window.scroll(0, 0);
                            document.title += "scroll-done";
                        }
                    }
                    setTimeout(f, 1000);
                })();
            """)
        time.sleep(2)
        for i in range(30):
            if "scroll-done" in driver.title:
                break
            driver.save_screenshot('base/graf/{}.png'.format(message.from_user.id))

    except Exception as ex:
        logger.debug(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    get_graf()
