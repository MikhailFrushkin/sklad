import json
import time

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from data.config import path
from handlers.users.back import back
from keyboards.default import menu
from keyboards.default.menu import second_menu
from keyboards.inline.actions_groups import actions
from loader import dp, bot
from state.states import Action


def parse_actions():
    city = {'city_id': "8056649", 'xml_id': "814", 'name': "Новосибирск"}
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
        '_dvs': '0:l4xkbjx9:75Gt_ixzEVwU2DTAN92jc8GG03a3QNjB',
        'PHPSESSID': '21tuagsti48ock048eu1cnn161',
        'BITRIX_SM_ab_test_multi': '%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22A%22%7D%2C%22reg_bk_and_yz%22%3A%7B%22ID%22%3A%228122416%22%2C%22NAME%22%3A%22reg_bk_and_yz%22%2C%22GROUP%22%3A%22A%22%7D%2C%22KS%22%3A%7B%22ID%22%3A%228116774%22%2C%22NAME%22%3A%22KS%22%2C%22GROUP%22%3A%22%22%7D%2C%223d%22%3A%7B%22ID%22%3A%228123834%22%2C%22NAME%22%3A%223d%22%2C%22GROUP%22%3A%22%22%7D%2C%22ar%22%3A%7B%22ID%22%3A%228123836%22%2C%22NAME%22%3A%22ar%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_basket%22%3A%7B%22ID%22%3A%228362213%22%2C%22NAME%22%3A%22rr_basket%22%2C%22GROUP%22%3A%22%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228362535%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22B%22%7D%2C%22credit_new_widget%22%3A%7B%22ID%22%3A%228324699%22%2C%22NAME%22%3A%22credit_new_widget%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228270671%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22B%22%7D%2C%22alter_sort%22%3A%7B%22ID%22%3A%228377079%22%2C%22NAME%22%3A%22alter_sort%22%2C%22GROUP%22%3A%22A%22%7D%2C%22checkbox%22%3A%7B%22ID%22%3A%227971955%22%2C%22NAME%22%3A%22checkbox%22%2C%22GROUP%22%3A%22A%22%7D%2C%22anyquery%22%3A%7B%22ID%22%3A%228392557%22%2C%22NAME%22%3A%22anyquery%22%2C%22GROUP%22%3A%22B%22%7D%7D',
        'BITRIX_SM_SOUND_LOGIN_PLAYED': 'Y',
        'dSesn': 'b5230dd3-4caa-708d-fce8-5a5267fcc8d9',
        'iwaf_fingerprint': '55c49ce9f14c551ca02458bb6e3ca0b9',
    }

    headers = {
        'authority': 'hoff.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json;charset=utf-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'current_location_id=3922; current_city=814; __exponea_etc__=82a9d7d9-7aae-b963-9a2c-b86e4fde012a; current_location_data=a%3A4%3A%7Bs%3A5%3A%22chain%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A68%3Bi%3A1%3Bi%3A3922%3B%7Ds%3A4%3A%22name%22%3Bs%3A22%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A9%3A%22full_name%22%3Bs%3A57%3A%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%2C%20%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%3Bs%3A11%3A%22location_id%22%3Bi%3A3922%3B%7D; _userGUID=0:l2spt324:7x9FU0d4NWXsPZP~uRnBeHM3i6v2J0AA; banner-cookie=1; BITRIX_SM_UIDH=40a68964cb044eb1b5bf8970e1d7727f; BITRIX_SM_UIDL=muxazila%40mail.ru; BITRIX_SM_USER_ID=6438425; BITRIX_SM_SALE_UID=1380282021; _dvs=0:l4xkbjx9:75Gt_ixzEVwU2DTAN92jc8GG03a3QNjB; PHPSESSID=21tuagsti48ock048eu1cnn161; BITRIX_SM_ab_test_multi=%7B%22aa06%22%3A%7B%22ID%22%3A%227710124%22%2C%22NAME%22%3A%22aa06%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa07%22%3A%7B%22ID%22%3A%227710127%22%2C%22NAME%22%3A%22aa07%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa08%22%3A%7B%22ID%22%3A%227710128%22%2C%22NAME%22%3A%22aa08%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa09%22%3A%7B%22ID%22%3A%227710129%22%2C%22NAME%22%3A%22aa09%22%2C%22GROUP%22%3A%22A%22%7D%2C%22aa10%22%3A%7B%22ID%22%3A%227710131%22%2C%22NAME%22%3A%22aa10%22%2C%22GROUP%22%3A%22A%22%7D%2C%22reg_bk_and_yz%22%3A%7B%22ID%22%3A%228122416%22%2C%22NAME%22%3A%22reg_bk_and_yz%22%2C%22GROUP%22%3A%22A%22%7D%2C%22KS%22%3A%7B%22ID%22%3A%228116774%22%2C%22NAME%22%3A%22KS%22%2C%22GROUP%22%3A%22%22%7D%2C%223d%22%3A%7B%22ID%22%3A%228123834%22%2C%22NAME%22%3A%223d%22%2C%22GROUP%22%3A%22%22%7D%2C%22ar%22%3A%7B%22ID%22%3A%228123836%22%2C%22NAME%22%3A%22ar%22%2C%22GROUP%22%3A%22%22%7D%2C%22kt_left%22%3A%7B%22ID%22%3A%228107330%22%2C%22NAME%22%3A%22kt_left%22%2C%22GROUP%22%3A%22B%22%7D%2C%22rr_basket%22%3A%7B%22ID%22%3A%228362213%22%2C%22NAME%22%3A%22rr_basket%22%2C%22GROUP%22%3A%22%22%7D%2C%22services%22%3A%7B%22ID%22%3A%228362535%22%2C%22NAME%22%3A%22services%22%2C%22GROUP%22%3A%22B%22%7D%2C%22credit_new_widget%22%3A%7B%22ID%22%3A%228324699%22%2C%22NAME%22%3A%22credit_new_widget%22%2C%22GROUP%22%3A%22A%22%7D%2C%22cartpopap%22%3A%7B%22ID%22%3A%228270671%22%2C%22NAME%22%3A%22cartpopap%22%2C%22GROUP%22%3A%22B%22%7D%2C%22alter_sort%22%3A%7B%22ID%22%3A%228377079%22%2C%22NAME%22%3A%22alter_sort%22%2C%22GROUP%22%3A%22A%22%7D%2C%22checkbox%22%3A%7B%22ID%22%3A%227971955%22%2C%22NAME%22%3A%22checkbox%22%2C%22GROUP%22%3A%22A%22%7D%2C%22anyquery%22%3A%7B%22ID%22%3A%228392557%22%2C%22NAME%22%3A%22anyquery%22%2C%22GROUP%22%3A%22B%22%7D%7D; BITRIX_SM_SOUND_LOGIN_PLAYED=Y; dSesn=b5230dd3-4caa-708d-fce8-5a5267fcc8d9; iwaf_fingerprint=55c49ce9f14c551ca02458bb6e3ca0b9',
        'referer': 'https://hoff.ru/catalog/tovary_dlya_doma/posuda/servirovka_stola/stolovye_pribory/nabory_stolovyh_priborov/nabor_lozhek_chaynykh_vanhopper_stolz_id8117007/?articul=80403863',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        'area': 'actions/index',
    }

    # response = requests.get('https://hoff.ru/vue/include-page/', params=params, cookies=cookies, headers=headers).json()
    # with open('action_group.json', 'w', encoding='utf-8') as file:
    #     json.dump(response, file, indent=4, ensure_ascii=False)
    # groups_dict = response.get('data').get('content')[1].get('custom:discount.sections').get('actions')
    groups_list = ['1181', '5359', '1184', '1182', '1020', '1140', '2269', '1183', '1185']
    for i in groups_list:
        logger.info('Сканируется группа {}'.format(i))
        time.sleep(5)

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
    await Action.show_product.set()


@dp.callback_query_handler(state=Action.show_product)
async def view_actionss(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'exit':
        await call.message.answer('Главное меню. Введите артикул. Пример: 80264335', reply_markup=menu)
        await state.reset_state()
        logger.info('Очистил state')
    else:
        try:
            with open('{}/base/json/action/action{}.json'.format(path, call.data), 'r',
                      encoding='utf-8') as file:
                catalog = json.load(file)
                count = 0
                logger.info('Пользователь {} {} запустил просмотр акций {}'.format(call.from_user.id,
                                                                                   call.from_user.first_name,
                                                                                   call.data))
                for item in catalog:
                    count += 1
                    await bot.send_photo(call.from_user.id, item["image"])
                    await bot.send_message(call.from_user.id, '{} {}\nСтарая цена: {} руб.\nНовая цена: {} руб.'
                                                              '\nСкидка: {}%'.format(
                        item["articul"], item["name"],
                        item["prices"]["old"], item["prices"]["new"], item["discount"]), reply_markup=second_menu)

                    if count == 10:
                        break
                    time.sleep(0.5)
        except Exception as ex:
            logger.debug(ex)
        finally:
            await back(call.message, state)


def main():
    parse_actions()


if __name__ == '__main__':
    main()
