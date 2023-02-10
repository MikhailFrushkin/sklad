import json
import os
import pprint
import re

import requests
from loguru import logger

from data.config import path

pp = pprint.PrettyPrinter(indent=4)


def get_id(art):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://hoff.ru',
        'Referer': 'https://hoff.ru/catalog/tovary_dlya_doma/shtory/karnizy_dlya_shtor/gotovye_karnizy/potolochnye_karnizy/karniz_dvukhryadnyy_optima_id2792999/?articul=80071767',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'apiKey': '919JS81645',
        'st': '{}'.format(art),
        'productsSize': '3',
        'showUnavailable': 'false',
        'regionId': '814',
    }

    response = requests.get('https://autocomplete.diginetica.net/autocomplete', params=params, headers=headers).json()
    return response.get('products')[0].get('link_url')


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
            # pattern = r'\Bid\d*'
            # print('Сканирование ', art)
            # id_art = re.search(pattern, get_id(art))[0][2:]
            # print(id_art)
            cookies = {
                'current_location_id': '3922',
                'current_city': '814',
                'BITRIX_SM_CUR_ORDER_IDS': '%5B%5D',
                '__exponea_etc__': 'd66337c2-81e1-6c94-2e64-e4eb4ced4bc4',
                'current_location_data': 'a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D',
                'digi_uc': 'W1sidiIsIjgwMzIwOTMzIiwxNjc0OTIwOTM0OTg1XSxbInYiLCI4MDQxMzQ0MiIsMTY3NDkyMDM0NzA2OF0sWyJ2IiwiODA0NDU3MDYiLDE2NzQ5MTk5MjkwNzBdLFsidiIsIjgwMzQ4NzQyIiwxNjc0MzA1Mzg1NDg0XSxbInYiLCI4MDMzODE3MyIsMTY3NDMwNDgzNDIxNl0sWyJ2IiwiODAzMDU5NzEiLDE2NzQzMDQ2NTY0MzRdLFsidiIsIjgwMjc5NjczIiwxNjc0MzAyMDE1MDg4XSxbInYiLCI4MDMyNDcwMyIsMTY3NDMwMTQxMzQxN10sWyJ2IiwiODA0NDA4NzYiLDE2NzQyOTk4NTg4NTJdLFsidiIsIjgwNTMwMDQzIiwxNjc0Mjg2OTA5NzM3XSxbInYiLCI4MDMwMTMzMSIsMTY3NDI4Njg5MTEzMV0sWyJ2IiwiODAyODczOTciLDE2NzQyODY4NzYyMDNdLFsidiIsIjgwMzQyMzAyIiwxNjc0Mjc5NTY2MDk3XSxbInYiLCI4MDUzMzY4NiIsMTY3NDI3OTQxMzY1Ml0sWyJ2IiwiODA0NTMwOTIiLDE2NzQyNzg5NTgwNjldLFsidiIsIjgwMzQ4NDY4IiwxNjc0Mjc4OTU0Mjc2XSxbInYiLCI4MDQ0NTAwNCIsMTY3NDI3ODYyOTc1MV0sWyJ2IiwiODA0NTQ4ODkiLDE2NzQyNzcxOTUyOTNdLFsidiIsIjgwMzIwODYxIiwxNjc0MjMyNTUwNDAwXSxbInYiLCI4MDMzNzY2MSIsMTY3NDIzMTQ4NTgwNF0sWyJ2IiwiODAzNDI0ODQiLDE2NzQ5MjEwMDU2NjVdXQ==',
                'BITRIX_SM_ab_test_multi': '%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_basket%22%3A%7B%22ID%22%3A%228362213%22%2C%22NAME%22%3A%22rr_basket%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_popup%22%3A%7B%22ID%22%3A%228413423%22%2C%22NAME%22%3A%22rr_popup%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aaaa%22%3A%7B%22ID%22%3A%228423545%22%2C%22NAME%22%3A%22aaaa%22%2C%22GROUP%22%3A%22B%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228468431%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22A%22%7D%2C%22quotas_sku%22%3A%7B%22ID%22%3A%228522979%22%2C%22NAME%22%3A%22quotas_sku%22%2C%22GROUP%22%3A%22A%22%7D%2C%22anyquery%22%3A%7B%22ID%22%3A%228525703%22%2C%22NAME%22%3A%22anyquery%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228544915%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22A%22%7D%2C%22main1%22%3A%7B%22ID%22%3A%228631187%22%2C%22NAME%22%3A%22main1%22%2C%22GROUP%22%3A%22B%22%7D%2C%22new_billing%22%3A%7B%22ID%22%3A%228696669%22%2C%22NAME%22%3A%22new_billing%22%2C%22GROUP%22%3A%22%22%7D%2C%22search_source2%22%3A%7B%22ID%22%3A%228735281%22%2C%22NAME%22%3A%22search_source2%22%2C%22GROUP%22%3A%22A%22%7D%2C%22KS%22%3A%7B%22ID%22%3A%228116774%22%2C%22NAME%22%3A%22KS%22%2C%22GROUP%22%3A%22%22%7D%2C%22preview_description%22%3A%7B%22ID%22%3A%228845505%22%2C%22NAME%22%3A%22preview_description%22%2C%22GROUP%22%3A%22%22%7D%2C%22alter_sort%22%3A%7B%22ID%22%3A%228849629%22%2C%22NAME%22%3A%22alter_sort%22%2C%22GROUP%22%3A%22A%22%7D%2C%22dates%22%3A%7B%22ID%22%3A%227895663%22%2C%22NAME%22%3A%22dates%22%2C%22GROUP%22%3A%22%22%7D%2C%22abc_bb_za_email%22%3A%7B%22ID%22%3A%228897565%22%2C%22NAME%22%3A%22abc_bb_za_email%22%2C%22GROUP%22%3A%22%22%7D%7D',
                'PHPSESSID': 'scslom5f5nvgr05785uci2i9on',
                'BITRIX_SM_UIDH': 'ce981f2c7b019287933f2b95a1055b98',
                'BITRIX_SM_UIDL': 'muxazila%40mail.ru',
                'BITRIX_SM_USER_ID': '6438425',
                'BITRIX_SM_SALE_UID': '1380282021',
                'BITRIX_SM_SOUND_LOGIN_PLAYED': 'Y',
                '_dvs': '0:ldoogs3m:5dkVSNYewhKTZE~FVdGZOlOklqOCnN5A',
                'iwaf_fingerprint': '80ea54c2ceafed23bfdbd53be86b785a',
            }

            headers = {
                'authority': 'hoff.ru',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'referer': 'https://hoff.ru/catalog/tovary_dlya_doma/tekstil/tekstil_dlya_vannoy/tapochki/pantolety_detskie_k_ch_o_id8217547/?articul=80438452',
                'sec-ch-ua': '"Chromium";v="108", "Opera";v="94", "Not)A;Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
                'x-requested-with': 'XMLHttpRequest',
            }

            json_data = {
                'articul': art
            }

            response = requests.post('https://hoff.ru/vue/search_titles_articul/', cookies=cookies, headers=headers,
                                     json=json_data).json()
            art_id = response.get('data').get('items')[0].get('id')
            params = {
                'id': art_id,
                'articul': f'{art}/json',
            }

            response = requests.get('https://hoff.ru/vue/catalog/product/',
                                    params=params, cookies=cookies, headers=headers).json()
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

            with open("{}/base/json/{}.json".format(path, art), "w", encoding='utf-8') as write_file:
                print(f'отсканирован {art}')
                json.dump(data, write_file, indent=4, ensure_ascii=False)
        except Exception as ex:
            logger.error(ex)
        return data


def main():
    list_art = [
        80071767,
        # 80305971,
        # 80321925,
        # 80322478,
        # 80322557,
        # 80323254,
        # 80324703,

    ]
    for i in list_art:
        print(parse(i))


if __name__ == '__main__':
    main()
