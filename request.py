import requests
import json


def get_data(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept - encoding': 'gzip, deflate, br',
        'accept - language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache - control': 'no - cache',
        'user - agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)

    with open('search.html', 'w', encoding='utf-8') as file:
        file.write(response.text)


def main():
    get_data('https://hoff.ru/vue/search/?fromSearch=direct&search=80264355&redirect_search=true')


if __name__ == '__main__':
    main()
