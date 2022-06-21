import json

import requests
from loguru import logger


def parse(art):
    cookies = {
        'current_location_id': '3922',
        'current_city': '814',
        '__exponea_etc__': '82a9d7d9-7aae-b963-9a2c-b86e4fde012a',
        'BITRIX_SM_SALE_UID': '1454797463',
        'current_location_data': 'a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D',
        '_userGUID': '0:l2spt324:7x9FU0d4NWXsPZP~uRnBeHM3i6v2J0AA',
        'banner-cookie': '1',
        'BITRIX_SM_ab_test_multi': '%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22A%22%7D%2C%22reg_bk_and_yz%22%3A%7B%22ID%22%3A%228122416%22%2C%22NAME%22%3A%22reg_bk_and_yz%22%2C%22GROUP%22%3A%22A%22%7D%2C%22KS%22%3A%7B%22ID%22%3A%228116774%22%2C%22NAME%22%3A%22KS%22%2C%22GROUP%22%3A%22%22%7D%2C%223d%22%3A%7B%22ID%22%3A%228123834%22%2C%22NAME%22%3A%223d%22%2C%22GROUP%22%3A%22%22%7D%2C%22ar%22%3A%7B%22ID%22%3A%228123836%22%2C%22NAME%22%3A%22ar%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_basket%22%3A%7B%22ID%22%3A%228362213%22%2C%22NAME%22%3A%22rr_basket%22%2C%22GROUP%22%3A%22%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228362535%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22B%22%7D%2C%22credit_new_widget%22%3A%7B%22ID%22%3A%228324699%22%2C%22NAME%22%3A%22credit_new_widget%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228270671%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22B%22%7D%2C%22alter_sort%22%3A%7B%22ID%22%3A%228377079%22%2C%22NAME%22%3A%22alter_sort%22%2C%22GROUP%22%3A%22A%22%7D%7D',
        'PHPSESSID': 'bnjse0rjlck3uaqafhq15qsk10',
        'iwaf_fingerprint': '55c49ce9f14c551ca02458bb6e3ca0b9',
        'dSesn': '89dd2d5c-1345-097b-6518-507b8198507f',
        '_dvs': '0:l4npu0j4:6sjkLU2BB_1JPQZ1a62TGZxRecCHBC5J',
        'iwaf_click_event': '481x77',
    }

    headers = {
        'authority': 'hoff.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json;charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'current_location_id=3922; current_city=814; __exponea_etc__=82a9d7d9-7aae-b963-9a2c-b86e4fde012a; BITRIX_SM_SALE_UID=1454797463; current_location_data=a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D; _userGUID=0:l2spt324:7x9FU0d4NWXsPZP~uRnBeHM3i6v2J0AA; banner-cookie=1; BITRIX_SM_ab_test_multi=%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22A%22%7D%2C%22reg_bk_and_yz%22%3A%7B%22ID%22%3A%228122416%22%2C%22NAME%22%3A%22reg_bk_and_yz%22%2C%22GROUP%22%3A%22A%22%7D%2C%22KS%22%3A%7B%22ID%22%3A%228116774%22%2C%22NAME%22%3A%22KS%22%2C%22GROUP%22%3A%22%22%7D%2C%223d%22%3A%7B%22ID%22%3A%228123834%22%2C%22NAME%22%3A%223d%22%2C%22GROUP%22%3A%22%22%7D%2C%22ar%22%3A%7B%22ID%22%3A%228123836%22%2C%22NAME%22%3A%22ar%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_basket%22%3A%7B%22ID%22%3A%228362213%22%2C%22NAME%22%3A%22rr_basket%22%2C%22GROUP%22%3A%22%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228362535%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22B%22%7D%2C%22credit_new_widget%22%3A%7B%22ID%22%3A%228324699%22%2C%22NAME%22%3A%22credit_new_widget%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228270671%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22B%22%7D%2C%22alter_sort%22%3A%7B%22ID%22%3A%228377079%22%2C%22NAME%22%3A%22alter_sort%22%2C%22GROUP%22%3A%22A%22%7D%7D; PHPSESSID=bnjse0rjlck3uaqafhq15qsk10; iwaf_fingerprint=55c49ce9f14c551ca02458bb6e3ca0b9; dSesn=89dd2d5c-1345-097b-6518-507b8198507f; _dvs=0:l4npu0j4:6sjkLU2BB_1JPQZ1a62TGZxRecCHBC5J; iwaf_click_event=481x77',
        'origin': 'https://hoff.ru',
        'referer': 'https://hoff.ru/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'articul': art,
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
        print(characteristic)
        characteristic_list = []
        pictures_list = []
        for item in characteristic:
            characteristic_list.append(item)
        for i in pictures:
            pictures_list.append(i['src'])
        data = {
            'id_product': id_product,
            'articul': articul,
            'characteristic': characteristic_list,
            'url': url,
            'name': name,
            'pictures': pictures_list,
            'price': price
        }
    except Exception as ex:
        logger.debug('Нет товара на сайте =( {}'.format(ex))
        data = {
            'id_product': None,
            'articul': None,
            'url': None,
            'characteristic': {'name': '', 'value': ''},
            'name': 'Нет товара на сайте',
            'pictures': ['https://jackwharperconstruction.com/wp-content/uploads/9/c/9/9c980deb1f9f42ef2244b13de3aa118d.jpg'],
            'price': 0
        }
    return data


def main():
    parse('80430058')


if __name__ == '__main__':
    main()
