from selenium import webdriver
import re


def url_art():
    art = 80264355
    draiver = webdriver.Chrome()
    draiver.get('https://hoff.ru/vue/search/?fromSearch=direct&search={}&redirect_search=true'.format(art))
    text = draiver.page_source
    pattern = r'(?<=\\).+?["]'
    result = re.search(pattern, text)
    result_url = 'https://hoff.ru' + result[0][:-2]
    return result_url


