import json

import requests
from loguru import logger

from data.config import path


def parse(art):
    cookies = {
        'current_location_id': '3922',
        'current_city': '814',
        '__exponea_etc__': '82a9d7d9-7aae-b963-9a2c-b86e4fde012a',
        'current_location_data': 'a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D',
        '_userGUID': '0:l2spt324:7x9FU0d4NWXsPZP~uRnBeHM3i6v2J0AA',
        'banner-cookie': '1',
        'BITRIX_SM_UIDH': '40a68964cb044eb1b5bf8970e1d7727f',
        'BITRIX_SM_UIDL': 'muxazila%40mail.ru',
        'BITRIX_SM_USER_ID': '6438425',
        'BITRIX_SM_SALE_UID': '1380282021',
        'BITRIX_SM_ab_test_multi': '%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22A%22%7D%2C%22reg_bk_and_yz%22%3A%7B%22ID%22%3A%228122416%22%2C%22NAME%22%3A%22reg_bk_and_yz%22%2C%22GROUP%22%3A%22A%22%7D%2C%22KS%22%3A%7B%22ID%22%3A%228116774%22%2C%22NAME%22%3A%22KS%22%2C%22GROUP%22%3A%22%22%7D%2C%223d%22%3A%7B%22ID%22%3A%228123834%22%2C%22NAME%22%3A%223d%22%2C%22GROUP%22%3A%22%22%7D%2C%22ar%22%3A%7B%22ID%22%3A%228123836%22%2C%22NAME%22%3A%22ar%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_basket%22%3A%7B%22ID%22%3A%228362213%22%2C%22NAME%22%3A%22rr_basket%22%2C%22GROUP%22%3A%22%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228362535%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22B%22%7D%2C%22credit_new_widget%22%3A%7B%22ID%22%3A%228324699%22%2C%22NAME%22%3A%22credit_new_widget%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228270671%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22B%22%7D%2C%22alter_sort%22%3A%7B%22ID%22%3A%228377079%22%2C%22NAME%22%3A%22alter_sort%22%2C%22GROUP%22%3A%22A%22%7D%2C%22checkbox%22%3A%7B%22ID%22%3A%227971955%22%2C%22NAME%22%3A%22checkbox%22%2C%22GROUP%22%3A%22A%22%7D%2C%22anyquery%22%3A%7B%22ID%22%3A%228402103%22%2C%22NAME%22%3A%22anyquery%22%2C%22GROUP%22%3A%22A%22%7D%2C%22dates%22%3A%7B%22ID%22%3A%227895663%22%2C%22NAME%22%3A%22dates%22%2C%22GROUP%22%3A%22%22%7D%7D',
        '_dvs': '0:l4z2lgtz:lkzls14W49RWPR49EEEw21RI_9Z5lIaM',
        'PHPSESSID': 'tsg25bg6ah1c2i4reqt27o5072',
        'BITRIX_SM_SOUND_LOGIN_PLAYED': 'Y',
        'iwaf_fingerprint': '55c49ce9f14c551ca02458bb6e3ca0b9',
        'dSesn': 'a240ff0d-1082-eb5c-8080-8f8b522eaf3f',
    }

    headers = {
        'authority': 'hoff.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json;charset=utf-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'current_location_id=3922; current_city=814; __exponea_etc__=82a9d7d9-7aae-b963-9a2c-b86e4fde012a; current_location_data=a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D; _userGUID=0:l2spt324:7x9FU0d4NWXsPZP~uRnBeHM3i6v2J0AA; banner-cookie=1; BITRIX_SM_UIDH=40a68964cb044eb1b5bf8970e1d7727f; BITRIX_SM_UIDL=muxazila%40mail.ru; BITRIX_SM_USER_ID=6438425; BITRIX_SM_SALE_UID=1380282021; BITRIX_SM_ab_test_multi=%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22A%22%7D%2C%22reg_bk_and_yz%22%3A%7B%22ID%22%3A%228122416%22%2C%22NAME%22%3A%22reg_bk_and_yz%22%2C%22GROUP%22%3A%22A%22%7D%2C%22KS%22%3A%7B%22ID%22%3A%228116774%22%2C%22NAME%22%3A%22KS%22%2C%22GROUP%22%3A%22%22%7D%2C%223d%22%3A%7B%22ID%22%3A%228123834%22%2C%22NAME%22%3A%223d%22%2C%22GROUP%22%3A%22%22%7D%2C%22ar%22%3A%7B%22ID%22%3A%228123836%22%2C%22NAME%22%3A%22ar%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_basket%22%3A%7B%22ID%22%3A%228362213%22%2C%22NAME%22%3A%22rr_basket%22%2C%22GROUP%22%3A%22%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228362535%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22B%22%7D%2C%22credit_new_widget%22%3A%7B%22ID%22%3A%228324699%22%2C%22NAME%22%3A%22credit_new_widget%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228270671%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22B%22%7D%2C%22alter_sort%22%3A%7B%22ID%22%3A%228377079%22%2C%22NAME%22%3A%22alter_sort%22%2C%22GROUP%22%3A%22A%22%7D%2C%22checkbox%22%3A%7B%22ID%22%3A%227971955%22%2C%22NAME%22%3A%22checkbox%22%2C%22GROUP%22%3A%22A%22%7D%2C%22anyquery%22%3A%7B%22ID%22%3A%228402103%22%2C%22NAME%22%3A%22anyquery%22%2C%22GROUP%22%3A%22A%22%7D%2C%22dates%22%3A%7B%22ID%22%3A%227895663%22%2C%22NAME%22%3A%22dates%22%2C%22GROUP%22%3A%22%22%7D%7D; _dvs=0:l4z2lgtz:lkzls14W49RWPR49EEEw21RI_9Z5lIaM; PHPSESSID=tsg25bg6ah1c2i4reqt27o5072; BITRIX_SM_SOUND_LOGIN_PLAYED=Y; iwaf_fingerprint=55c49ce9f14c551ca02458bb6e3ca0b9; dSesn=a240ff0d-1082-eb5c-8080-8f8b522eaf3f',
        'referer': 'https://hoff.ru/catalog/tovary_dlya_doma/posuda/servirovka_stola/stolovye_pribory/nabory_stolovyh_priborov/nabor_lozhek_chaynykh_vanhopper_stolz_id8117007/?articul=80403863',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'articul': art
    }

    try:
        response = requests.post('https://hoff.ru/vue/search_titles_articul/', cookies=cookies, headers=headers,
                                 json=json_data).json()
        id_product = response.get('data').get('items')[0].get('id')
        articul = response.get('data').get('items')[0].get('articul')
        url = response.get('data').get('items')[0].get('url')
        price = response.get('data').get('items')[0].get('prices').get('new')

        params = {
            'id': id_product,
            'articul': articul,
        }
        response = requests.get('https://hoff.ru/vue/catalog/product/',
                                params=params, cookies=cookies, headers=headers).json()
        name = response.get('data').get('name')
        pictures = response.get('data').get('slider').get('pictures')
        characteristic = response.get('data').get('characteristic_tab').get('items')
        slider_picture = response.get('data').get('slider_picture')
        characteristic_list = []
        pictures_list = []
        for item in characteristic:
            characteristic_list.append('{} {}'.format(item['name'], item['value']))
        for i in pictures:
            pictures_list.append(i['src'])
        data = {
            'id_product': id_product,
            'articul': articul,
            'characteristic': characteristic_list,
            'url': url,
            'name': name,
            'pictures': pictures_list,
            'slider_picture': slider_picture,
            'price': price
        }
        with open("{}/base/json/{}.json".format(path, art), "w", encoding='utf-8') as write_file:
            json.dump(data, write_file, indent=4, ensure_ascii=False)
        return data
    except Exception as ex:
        logger.debug('Нет товара на сайте =( {} или 1 парсер отвалился'.format(ex))


def main():
    parse('80440871')


if __name__ == '__main__':
    main()
