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
from utils.open_exsel import search_all_sklad


def parse_actions():
    # city = {'city_id': "8056649", 'xml_id': "814", 'name': "Новосибирск"}
    cookies = {
        '_userGUID': '0:l6217nxl:ONd22xw2GGQqPr5D5Ens7kc1GFjZVk64',
        '__exponea_etc__': '57e32f2a-ba60-d4dc-d067-27d24eba3882',
        'CUR_ORDER_IDS': '%5B%5D',
        'current_location_id': '3922',
        'current_city': '814',
        'current_location_data': 'a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D',
        'PHPSESSID': 'eobshp3n58ci9vstoc4aft7hav',
        'BITRIX_SM_ab_test_multi': '%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22B%22%7D%2C%22dates%22%3A%7B%22ID%22%3A%227895663%22%2C%22NAME%22%3A%22dates%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22A%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228468431%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22A%22%7D%2C%22anyquery%22%3A%7B%22ID%22%3A%228525703%22%2C%22NAME%22%3A%22anyquery%22%2C%22GROUP%22%3A%22A%22%7D%2C%22rr_popup%22%3A%7B%22ID%22%3A%228413423%22%2C%22NAME%22%3A%22rr_popup%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228544915%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aaaa%22%3A%7B%22ID%22%3A%228423545%22%2C%22NAME%22%3A%22aaaa%22%2C%22GROUP%22%3A%22B%22%7D%2C%22quotas_sku%22%3A%7B%22ID%22%3A%228522979%22%2C%22NAME%22%3A%22quotas_sku%22%2C%22GROUP%22%3A%22A%22%7D%2C%22search_source2%22%3A%7B%22ID%22%3A%228494465%22%2C%22NAME%22%3A%22search_source2%22%2C%22GROUP%22%3A%22%22%7D%2C%22vmeste_pokupayut%22%3A%7B%22ID%22%3A%228431927%22%2C%22NAME%22%3A%22vmeste_pokupayut%22%2C%22GROUP%22%3A%22%22%7D%2C%22hity_prodazh%22%3A%7B%22ID%22%3A%228351207%22%2C%22NAME%22%3A%22hity_prodazh%22%2C%22GROUP%22%3A%22%22%7D%2C%22smart_filters%22%3A%7B%22ID%22%3A%228642223%22%2C%22NAME%22%3A%22smart_filters%22%2C%22GROUP%22%3A%22A%22%7D%2C%22gift_cards%22%3A%7B%22ID%22%3A%228639641%22%2C%22NAME%22%3A%22gift_cards%22%2C%22GROUP%22%3A%22A%22%7D%2C%22complementary%22%3A%7B%22ID%22%3A%228477299%22%2C%22NAME%22%3A%22complementary%22%2C%22GROUP%22%3A%22B%22%7D%2C%22video_listing%22%3A%7B%22ID%22%3A%228540227%22%2C%22NAME%22%3A%22video_listing%22%2C%22GROUP%22%3A%22%22%7D%2C%22setka%22%3A%7B%22ID%22%3A%228631141%22%2C%22NAME%22%3A%22setka%22%2C%22GROUP%22%3A%22%22%7D%2C%22main1%22%3A%7B%22ID%22%3A%228631187%22%2C%22NAME%22%3A%22main1%22%2C%22GROUP%22%3A%22%22%7D%2C%22fix_filters%22%3A%7B%22ID%22%3A%228642233%22%2C%22NAME%22%3A%22fix_filters%22%2C%22GROUP%22%3A%22B%22%7D%7D',
        'iwaf_fingerprint': '80ea54c2ceafed23bfdbd53be86b785a',
        'dSesn': 'f0427f7a-a429-8028-2e69-8a63b25e45d0',
        '_dvs': '0:l9e4atmy:0hRXJF2xhXciYHnMPkVbfLZsGwWMr7Md',
        'BITRIX_SM_SALE_UID': '1528409113',
        'iwaf_scroll_event': '496',
    }

    headers = {
        'authority': 'hoff.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json;charset=utf-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_userGUID=0:l6217nxl:ONd22xw2GGQqPr5D5Ens7kc1GFjZVk64; __exponea_etc__=57e32f2a-ba60-d4dc-d067-27d24eba3882; CUR_ORDER_IDS=%5B%5D; current_location_id=3922; current_city=814; current_location_data=a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D; PHPSESSID=eobshp3n58ci9vstoc4aft7hav; BITRIX_SM_ab_test_multi=%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22B%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22B%22%7D%2C%22dates%22%3A%7B%22ID%22%3A%227895663%22%2C%22NAME%22%3A%22dates%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22A%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228468431%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22A%22%7D%2C%22anyquery%22%3A%7B%22ID%22%3A%228525703%22%2C%22NAME%22%3A%22anyquery%22%2C%22GROUP%22%3A%22A%22%7D%2C%22rr_popup%22%3A%7B%22ID%22%3A%228413423%22%2C%22NAME%22%3A%22rr_popup%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228544915%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aaaa%22%3A%7B%22ID%22%3A%228423545%22%2C%22NAME%22%3A%22aaaa%22%2C%22GROUP%22%3A%22B%22%7D%2C%22quotas_sku%22%3A%7B%22ID%22%3A%228522979%22%2C%22NAME%22%3A%22quotas_sku%22%2C%22GROUP%22%3A%22A%22%7D%2C%22search_source2%22%3A%7B%22ID%22%3A%228494465%22%2C%22NAME%22%3A%22search_source2%22%2C%22GROUP%22%3A%22%22%7D%2C%22vmeste_pokupayut%22%3A%7B%22ID%22%3A%228431927%22%2C%22NAME%22%3A%22vmeste_pokupayut%22%2C%22GROUP%22%3A%22%22%7D%2C%22hity_prodazh%22%3A%7B%22ID%22%3A%228351207%22%2C%22NAME%22%3A%22hity_prodazh%22%2C%22GROUP%22%3A%22%22%7D%2C%22smart_filters%22%3A%7B%22ID%22%3A%228642223%22%2C%22NAME%22%3A%22smart_filters%22%2C%22GROUP%22%3A%22A%22%7D%2C%22gift_cards%22%3A%7B%22ID%22%3A%228639641%22%2C%22NAME%22%3A%22gift_cards%22%2C%22GROUP%22%3A%22A%22%7D%2C%22complementary%22%3A%7B%22ID%22%3A%228477299%22%2C%22NAME%22%3A%22complementary%22%2C%22GROUP%22%3A%22B%22%7D%2C%22video_listing%22%3A%7B%22ID%22%3A%228540227%22%2C%22NAME%22%3A%22video_listing%22%2C%22GROUP%22%3A%22%22%7D%2C%22setka%22%3A%7B%22ID%22%3A%228631141%22%2C%22NAME%22%3A%22setka%22%2C%22GROUP%22%3A%22%22%7D%2C%22main1%22%3A%7B%22ID%22%3A%228631187%22%2C%22NAME%22%3A%22main1%22%2C%22GROUP%22%3A%22%22%7D%2C%22fix_filters%22%3A%7B%22ID%22%3A%228642233%22%2C%22NAME%22%3A%22fix_filters%22%2C%22GROUP%22%3A%22B%22%7D%7D; iwaf_fingerprint=80ea54c2ceafed23bfdbd53be86b785a; dSesn=f0427f7a-a429-8028-2e69-8a63b25e45d0; _dvs=0:l9e4atmy:0hRXJF2xhXciYHnMPkVbfLZsGwWMr7Md; BITRIX_SM_SALE_UID=1528409113; iwaf_scroll_event=496',
        'referer': 'https://hoff.ru/catalog/tovary_dlya_doma/dekor/?tovary_so_skidkoi=1&sort=discount_desc',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Opera";v="91", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.77',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        'area': 'actions/index',
    }

    groups_list = ['1181', '5359', '1184', '1182', '1020', '1140', '2269', '1183', '1185']
    offset = 1
    for i in groups_list:
        logger.info('Сканируется группа {}'.format(i))
        time.sleep(3)
        catalog = []
        for j in range(3):
            params = {
                'category_id': i,
                'limit': '30',
                'offset': str(offset*30),
                'showCount': 'true',
                'type': 'product_list',
                'tovary_so_skidkoi': '1',
                'sort': 'discount_desc',
            }
            try:
                response = requests.get('https://hoff.ru/vue/catalog/section/',
                                        params=params, cookies=cookies, headers=headers).json()
                producs = response.get('data').get('items')
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
                offset += 1

            except Exception as ex:
                logger.debug(ex)
        offset = 1
        with open('{}/base/json/action/action{}.json'.format(path, params['category_id']), 'w',
                  encoding='utf-8') as file:
            json.dump(catalog, file, ensure_ascii=False, indent=4)


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
            await bot.send_message(call.from_user.id, 'Выберите количество товаров к показу:', reply_markup=product_num)

            await Action.show_product.set()
            data['group'] = call.data


@dp.callback_query_handler(state=Action.show_product)
async def view_actionss(call: types.CallbackQuery, state: FSMContext):
    id = call.from_user.id
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

                        sklad_list = ['011_825', '012_825', 'A11_825', 'V_Sales', 'RDiff']
                        full_block = ['Остатки на магазине:']
                        try:
                            for i in sklad_list:
                                cells = search_all_sklad(item["articul"], i)
                                if cells:
                                    for j in cells:
                                        full_block.append(j)
                            if len(full_block) > 1:
                                count += 1
                                await bot.send_photo(call.from_user.id, item["image"])
                                await bot.send_message(call.from_user.id,
                                                       '{} {}\nСтарая цена: {} руб.\nНовая цена: {} руб.'
                                                       '\nСкидка: {}%'.format(item["articul"], item["name"],
                                                                              item["prices"]["old"],
                                                                              item["prices"]["new"],
                                                                              item["discount"]),
                                                       reply_markup=second_menu)
                                await bot.send_message(id, '\n'.join(full_block))
                                time.sleep(1)
                        except Exception as ex:
                            logger.debug('Ошибка при выводе ячеек в гланом меню {}', ex)

                        if count == int(call.data) or count == 20:
                            break
            except Exception as ex:
                logger.debug(ex)
            finally:
                await back(call, state)


def main():
    parse_actions()


if __name__ == '__main__':
    main()
