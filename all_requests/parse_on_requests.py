import json
import os

import requests
from loguru import logger

from data.config import path


def parse(art):
    data = {
        'articul': art,
        'characteristic': [],
        'url': '',
        'name': 'name',
        'pictures': ['https://upload.wikimedia.org/wikipedia/commons/9/'
                     '9a/%D0%9D%D0%B5%D1%82_%D1%84%D0%BE%D1%82%D0%BE.png'],
        'price': 0,
        'box': ['1 упаковка']
    }
    characteristic_result = []
    if os.path.exists("{}/base/json/{}.json".format(path, art)):
        with open("{}/base/json/{}.json".format(path, art), 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    else:
        try:
            print('Сканирование ', art)
            params = {
                'articul': art,
            }
            response = requests.get('https://hoff.ru/vue/catalog/product/', params=params).json()
            with open("json.json", "w", encoding='utf-8') as write_file:
                json.dump(response, write_file, indent=4, ensure_ascii=False)
            data['articul'] = response.get('data').get('articul')
            data['url'] = response.get('data').get('meta').get('canonical')
            data['name'] = response.get('data').get('name')
            data['pictures'] = [i['src'] for i in response.get('data').get('slider').get('pictures')]
            data['price'] = response.get('data').get('price')

            characteristic = response.get('data').get('characteristic_by_tab').get('properties')
            if len(characteristic) == 0:
                characteristic_result = ['{}-{}'.format(i['name'], i['value']) for i in
                                  response.get('data').get('characteristic_tab').get('items')]
            else:
                for i in characteristic:
                    for j in i['items']:
                        print(j)
                        characteristic_result.append('{}-{}'.format(j['name'], j['value']))
            data['characteristic'] = characteristic_result
            try:
                box = response.get('data').get('characteristic_tab').get('packages')
                if box:
                    data['box'] = list()
                    for item in box:
                        data['box'].append(
                            '{}-{}x{}x{}({})'.format(item['title'], item['width'], item['height'], item['depth'],
                                                     item['weight']))
            except Exception as ex:
                logger.error(ex)


        except Exception as ex:
            logger.error('Не удалось найти на сайте: {}{}'.format(art, ex))

        with open("{}/base/json/{}.json".format(path, art), "w", encoding='utf-8') as write_file:
            json.dump(data, write_file, indent=4, ensure_ascii=False)

        return data


def main():
    list_art = [
        80304912,
        # 80305971,
        # 80321925,
        # 80322478,
        # 80322557,
        # 80323254,
        # 80324703,
        80445706

    ]
    for i in list_art:
        print(parse(i))


if __name__ == '__main__':
    main()
