import json

from database.connect_DB import *
from database.date import *
import pandas as pd


def read_all_base():
    sklad_list = ['011_825', '012_825', 'A11_825', 'V_Sales', 'RDiff']
    art_dict = {}
    for sklad in sklad_list:
        with open('{}/files/file_old_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Код \nноменклатуры'] in art_dict.keys():
                    art_dict[row['Код \nноменклатуры']].append({
                        row['Местоположение']: row['Физические \nзапасы']
                    })
                else:
                    art_dict[row['Код \nноменклатуры']] = [{
                        row['Местоположение']: row['Физические \nзапасы']
                    }]
    with open('{}/files/old_base_arts.json'.format(path), 'w', encoding='utf-8') as file:
        json.dump(art_dict, file, ensure_ascii=False, indent=4)

    art_dict = {}
    for sklad in sklad_list:
        with open('{}/files/file_{}.csv'.format(path, sklad), newline='', encoding='utf-8') as csvfile2:
            reader2 = csv.DictReader(csvfile2)
            for row in reader2:
                if row['Код \nноменклатуры'] in art_dict.keys():
                    art_dict[row['Код \nноменклатуры']].append({
                        row['Местоположение']: row['Физические \nзапасы']
                    })
                else:
                    art_dict[row['Код \nноменклатуры']] = [{
                        row['Местоположение']: row['Физические \nзапасы']
                    }]
    with open('{}/files/new_base_arts.json'.format(path), 'w', encoding='utf-8') as file:
        json.dump(art_dict, file, ensure_ascii=False, indent=4)
    new_rdiff()


def new_rdiff():
    rdiff_list = []
    rdiff_list_new = []
    with open('{}/files/file_old_RDiff.csv'.format(path), newline='', encoding='utf-8') as csvfile_old:
        reader_old = csv.DictReader(csvfile_old)
        for row in reader_old:
            rdiff_list.append([row['Код \nноменклатуры'], row['Описание товара'], row['Физические \nзапасы']])
    with open('{}/files/file_RDiff.csv'.format(path), newline='', encoding='utf-8') as csvfile_new:
        reader_new = csv.DictReader(csvfile_new)
        for row2 in reader_new:
            temp = [row2['Код \nноменклатуры'], row2['Описание товара'], row2['Физические \nзапасы']]
            if temp not in rdiff_list:
                rdiff_list_new.append(row2['Код \nноменклатуры'])
    # print(len(rdiff_list_new))
    view_place_rdiff(rdiff_list_new)
    matching_rdiff()


def view_place_rdiff(rdiff_list_new):
    with open('{}/files/new_base_arts.json'.format(path), 'r', encoding='utf-8') as file:
        data_new = json.load(file)
    with open('{}/files/old_base_arts.json'.format(path), 'r', encoding='utf-8') as file:
        data_old = json.load(file)
    data_place = {
    }

    for art in rdiff_list_new:
        try:
            data_place[art] = {}
            if art in data_new.keys():
                data_place[art]['new'] = data_new[art]
            if art in data_old.keys():
                data_place[art]['old'] = data_old[art]
        except KeyError as ex:
            logger.debug(art, ex)
    with open('{}/files/result.json'.format(path), 'w', encoding='utf-8') as file:
        json.dump(data_place, file, ensure_ascii=False, indent=4)


def matching_rdiff():
    with open('{}/files/result.json'.format(path), 'r', encoding='utf-8') as file:
        data_rdiff = json.load(file)
    art_list = [i for i, j in data_rdiff.items()]

    list_cell_art = {}
    for i in art_list:
        list_cell = []
        try:
            for old in data_rdiff.get(i).get('old'):
                list_cell.append(list(old.keys())[0])
        except Exception as ex:
            logger.debug('У артикула {} нет ячейки в старом файле {}'.format(i, ex))
        try:
            for new in data_rdiff.get(i).get('new'):
                list_cell.append(list(new.keys())[0])
        except Exception as ex:
            logger.debug('У артикула {} нет ячейки в новом файле {}'.format(i, ex))
        list_cell = sorted(list(set(list_cell)))
        list_cell_art[i] = list_cell
    result = {}
    for i in art_list:
        result_cells = []
        for cell in list_cell_art[i]:

            try:
                a = [int(list(item.values())[0]) for item in data_rdiff.get(i).get('old') if
                     cell == list(item.keys())[0]]
            except Exception:
                a = []
            try:
                b = [int(list(item.values())[0]) for item in data_rdiff.get(i).get('new') if
                     cell == list(item.keys())[0]]
            except Exception:
                b = []
            if len(a) == 0:
                list_num = [0, b[0], b[0]]
            elif len(b) == 0:
                list_num = [a[0], 0, -a[0]]
            else:
                list_num = [a[0], b[0], b[0] - a[0]]
            result_cells.append([cell, list_num])

        result[i] = result_cells
    # for key, value in result.items():
    #     print(key)
    #     for i in value:
    #         print('{} дельта: {}\nБыло: {} Стало: {}'.format(i[0], i[1][2], i[1][0], i[1][1]))
    with open('{}/files/output.json'.format(path), 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    return result


def new_rdiff_to_exsel():
    data = matching_rdiff()
    print(len(list(data.keys())))
    data2 = {
            'Артикул': [],
            'Старая ячейка': [],
            'Количество(с)': [],
            'Новая ячейка': [],
            'Количество(н)': [],
            'Дельта': []
    }
    count_art = 0
    for key, value in data.items():
        count = 0
        for i in value:
            if count == 0:
                data2['Артикул'].append(key)
            else:
                data2['Артикул'].append('')
            data2['Старая ячейка'].append(i[0])
            data2['Количество(с)'].append(i[1][0])
            data2['Новая ячейка'].append(i[0])
            data2['Количество(н)'].append(i[1][1])
            data2['Дельта'].append(i[1][2])
            count += 1
        count_art += 1
        if count_art != len(list(data.keys())):
            data2['Артикул'].append('')
            data2['Старая ячейка'].append('')
            data2['Количество(с)'].append('')
            data2['Новая ячейка'].append('')
            data2['Количество(н)'].append('')
            data2['Дельта'].append('')
            # data2['Артикул'].append('Артикул')
            # data2['Старая ячейка'].append('Старая ячейка')
            # data2['Количество(с)'].append('Количество(с)')
            # data2['Новая ячейка'].append('Новая ячейка')
            # data2['Количество(н)'].append('Количество(н)')
            # data2['Дельта'].append('Дельта')
    df_marks = pd.DataFrame(data2)
    writer = pd.ExcelWriter('{}/files/new_rdiff.xlsx'.format(path))
    df_marks.to_excel(writer, sheet_name='Сверка', index=False, na_rep='NaN')
    workbook = writer.book
    worksheet = writer.sheets['Сверка']
    cell_format = workbook.add_format()
    cell_format.set_align('center')
    cell_format.set_bold()
    cell_format.set_border(1)
    cell_format.set_num_format('[Green]General;[Red]-General;General')

    cell_format2 = workbook.add_format({'align': 'left',
                                        'valign': 'vcenter',
                                        'border': 1})

    cell_format3 = workbook.add_format({'align': 'center',
                                        'valign': 'vcenter',
                                        'border': 1})

    worksheet.set_column('A:A', 10, cell_format2)
    worksheet.set_column('B:B', 18, cell_format2)
    worksheet.set_column('D:D', 18, cell_format2)
    worksheet.set_column('C:C', 14, cell_format3)
    worksheet.set_column('E:E', 14, cell_format3)
    worksheet.set_column('F:F', 14, cell_format)
    writer.close()


if __name__ == '__main__':
    new_rdiff_to_exsel()
