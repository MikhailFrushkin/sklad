import requests


def main():
    url_list = ['https://hoff.ru/upload/iblock/3b3/3b31a67c01ee52d6754e31c39b42ed72.jpg',
                'https://hoff.ru/upload/iblock/612/612c53b6dfaad1be1e6ec83fafa54bda.jpg',
                'https://hoff.ru/upload/iblock/636/6367fc7e1930869b47c4d97c8b39bfff.jpg',
                'https://hoff.ru/upload/iblock/c71/c71bbdd034b67390313f759031a40039.jpg']
    for i in url_list:
        r = requests.get(i)
        print(r.status_code)


if __name__ == '__main__':
    main()
