import json
import time

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from data.config import path
from handlers.users.back import back
from keyboards.default.menu import second_menu
from keyboards.inline.action import product_num
from keyboards.inline.actions_groups import actions
from loader import dp, bot
from state.states import Action


def parse_actions():
    city = {'city_id': "8056649", 'xml_id': "814", 'name': "Новосибирск"}
    cookies = {
        'current_location_id': '3922',
        'current_city': '814',
        'current_location_data': 'a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D',
        'BITRIX_SM_SALE_UID': '1492353103',
        '_userGUID': '0:l3vgspid:9vBNTj8aTUicjc1ITcyA3Q3K0eoi1ZS7',
        '__exponea_etc__': '3894f658-9300-e055-98d0-466b3376dfbc',
        '_dvs': '0:l50bu63t:DQ~kcPDRr_UjRuFeGIBehpjLw_wqN6EJ',
        'PHPSESSID': 'mf4r8hl1khtq4g9appialjt9q8',
        'BITRIX_SM_ab_test_multi': '%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22B%22%7D%2C%22KS%22%3A%7B%22ID%22%3A%228116774%22%2C%22NAME%22%3A%22KS%22%2C%22GROUP%22%3A%22%22%7D%2C%22reg_bk_and_yz%22%3A%7B%22ID%22%3A%228122416%22%2C%22NAME%22%3A%22reg_bk_and_yz%22%2C%22GROUP%22%3A%22B%22%7D%2C%223d%22%3A%7B%22ID%22%3A%228123834%22%2C%22NAME%22%3A%223d%22%2C%22GROUP%22%3A%22%22%7D%2C%22ar%22%3A%7B%22ID%22%3A%228123836%22%2C%22NAME%22%3A%22ar%22%2C%22GROUP%22%3A%22%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228362535%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_basket%22%3A%7B%22ID%22%3A%228362213%22%2C%22NAME%22%3A%22rr_basket%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22B%22%7D%2C%22credit_new_widget%22%3A%7B%22ID%22%3A%228324699%22%2C%22NAME%22%3A%22credit_new_widget%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228270671%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22B%22%7D%2C%22alter_sort%22%3A%7B%22ID%22%3A%228377079%22%2C%22NAME%22%3A%22alter_sort%22%2C%22GROUP%22%3A%22A%22%7D%2C%22dates%22%3A%7B%22ID%22%3A%227895663%22%2C%22NAME%22%3A%22dates%22%2C%22GROUP%22%3A%22%22%7D%2C%22anyquery%22%3A%7B%22ID%22%3A%228402103%22%2C%22NAME%22%3A%22anyquery%22%2C%22GROUP%22%3A%22A%22%7D%7D',
        'dSesn': '8ff576f8-67a9-186a-df1d-9e4efac4a33c',
        'iwaf_fingerprint': '55c49ce9f14c551ca02458bb6e3ca0b9',
    }

    headers = {
        'authority': 'hoff.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json;charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'current_location_id=3922; current_city=814; current_location_data=a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D; BITRIX_SM_SALE_UID=1492353103; _userGUID=0:l3vgspid:9vBNTj8aTUicjc1ITcyA3Q3K0eoi1ZS7; __exponea_etc__=3894f658-9300-e055-98d0-466b3376dfbc; _dvs=0:l50bu63t:DQ~kcPDRr_UjRuFeGIBehpjLw_wqN6EJ; PHPSESSID=mf4r8hl1khtq4g9appialjt9q8; BITRIX_SM_ab_test_multi=%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22B%22%7D%2C%22KS%22%3A%7B%22ID%22%3A%228116774%22%2C%22NAME%22%3A%22KS%22%2C%22GROUP%22%3A%22%22%7D%2C%22reg_bk_and_yz%22%3A%7B%22ID%22%3A%228122416%22%2C%22NAME%22%3A%22reg_bk_and_yz%22%2C%22GROUP%22%3A%22B%22%7D%2C%223d%22%3A%7B%22ID%22%3A%228123834%22%2C%22NAME%22%3A%223d%22%2C%22GROUP%22%3A%22%22%7D%2C%22ar%22%3A%7B%22ID%22%3A%228123836%22%2C%22NAME%22%3A%22ar%22%2C%22GROUP%22%3A%22%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228362535%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_basket%22%3A%7B%22ID%22%3A%228362213%22%2C%22NAME%22%3A%22rr_basket%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22B%22%7D%2C%22credit_new_widget%22%3A%7B%22ID%22%3A%228324699%22%2C%22NAME%22%3A%22credit_new_widget%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228270671%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22B%22%7D%2C%22alter_sort%22%3A%7B%22ID%22%3A%228377079%22%2C%22NAME%22%3A%22alter_sort%22%2C%22GROUP%22%3A%22A%22%7D%2C%22dates%22%3A%7B%22ID%22%3A%227895663%22%2C%22NAME%22%3A%22dates%22%2C%22GROUP%22%3A%22%22%7D%2C%22anyquery%22%3A%7B%22ID%22%3A%228402103%22%2C%22NAME%22%3A%22anyquery%22%2C%22GROUP%22%3A%22A%22%7D%7D; dSesn=8ff576f8-67a9-186a-df1d-9e4efac4a33c; iwaf_fingerprint=55c49ce9f14c551ca02458bb6e3ca0b9',
        'origin': 'https://hoff.ru',
        'referer': 'https://hoff.ru/',
        'sec-ch-ua': '"Chromium";v="102", "Opera";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.53',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        'area': 'actions/index',
    }

    groups_list = ['1181', '5359', '1184', '1182', '1020', '1140', '2269', '1183', '1185']
    for i in groups_list:
        logger.info('Сканируется группа {}'.format(i))
        time.sleep(3)

        params = {
            'category_id': i,
            'limit': '30',
            'offset': '0',
            'showCount': 'true',
            'type': 'product_list',
            'tovary_so_skidkoi': '1',
            'sort': 'discount_desc',
        }
        try:
            response = requests.get('https://hoff.ru/vue/catalog/section/',
                                    params=params, cookies=cookies, headers=headers).json()
            producs = response.get('data').get('items')
            catalog = []
            for item in producs:
                catalog.append({
                    'articul': item['articul'],
                    'name': item['name'],
                    'image': item['image'],
                    'prices': {
                        'new': item['prices']['new'],
                        'old': item['prices']['old']
                    },
                    'discount': item['discount'],
                    'in_stock': item['in_stock']
                })
            with open('{}/base/json/action/action{}.json'.format(path, params['category_id']), 'w',
                      encoding='utf-8') as file:
                json.dump(catalog, file, ensure_ascii=False, indent=4)
        except Exception as ex:
            logger.debug(ex)


@dp.message_handler(content_types=['text'], state=Action.set_group)
async def view_actions(message, state):
    await bot.send_message(message.from_user.id, 'Выберите группу:', reply_markup=actions)
    await Action.set_num.set()


@dp.callback_query_handler(state=Action.set_num)
async def view_actionss(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == 'exit':
            await back(call, state)
        else:
            await bot.send_message(call.from_user.id, 'Выберите группу:', reply_markup=product_num)
            data['group'] = call.data
            await Action.show_product.set()


@dp.callback_query_handler(state=Action.show_product)
async def view_actionss(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == 'exit':
            await back(call, state)
        else:
            groups_list = [['Декор', '1181'], ['Зеркала', '5359'], ['Ковры', '1184'],
                           ['Освещение', '1182'], ['Посуда', '1020'], ['Текстиль', '1140'],
                           ['Товары для ванной', '2269'], ['Хозтовары', '1183'], ['Шторы и карнизы', '1185']]
            try:
                with open('{}/base/json/action/action{}.json'.format(path, data['group']), 'r',
                          encoding='utf-8') as file:
                    catalog = json.load(file)
                    count = 0
                    logger.info('Пользователь {} {} запустил просмотр акций {} {}'.format(call.from_user.id,
                                                                                          call.from_user.first_name,
                                                                                          [
                                                                                              i for i in groups_list
                                                                                              if data['group'] in i
                                                                                          ], call.data))
                    for item in catalog:
                        count += 1
                        await bot.send_photo(call.from_user.id, item["image"])
                        await bot.send_message(call.from_user.id, '{} {}\nСтарая цена: {} руб.\nНовая цена: {} руб.'
                                                                  '\nСкидка: {}%'.format(
                            item["articul"], item["name"],
                            item["prices"]["old"], item["prices"]["new"], item["discount"]), reply_markup=second_menu)

                        if count == int(call.data):
                            break
                        time.sleep(0.5)
            except Exception as ex:
                logger.debug(ex)
            finally:
                await back(call, state)


def main():
    parse_actions()


if __name__ == '__main__':
    main()
