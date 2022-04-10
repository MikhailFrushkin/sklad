import re
import time
from urllib.request import urlopen
import requests
import os

from requests_html import HTMLSession
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def main():
    art = 80264355
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    driver.get('https://hoff.ru/vue/search/?fromSearch=direct&search={}&redirect_search=true'.format(art))

    try:
        text = driver.page_source
        pattern = r'(?<=\\).+?["]'
        result = re.search(pattern, text)
        url_page1 = 'https://hoff.ru' + result[0][:-1]
        url = url_page1.replace('\\', '')
        time.sleep(5)
        get_photo('https://hoff.ru')

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def get_photo(url):
    session = HTMLSession()
    response = session.get(url)
    response.html.render(timeout=20)
    soup = bs(response.html.html, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Извлечено изображение"):
        img_url = img.attrs.get("src") or img.attrs.get("data-src") or img.attrs.get("data-original")
        print(img_url)
        if not img_url:

            continue

        urls.append(img_url)
    session.close()
    return urls


if __name__ == '__main__':
    main()
