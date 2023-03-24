import pandas as pd
from data.config import path

tg = '11'

def main():
    df = pd.read_csv(f'{path}/files/file_012_825.csv')
    df = df[df['Доступно'] > 0]
    cells_per_art = df.groupby('Код \nноменклатуры').size()
    cells_per_art = cells_per_art[cells_per_art > 2]
    cells_per_art = cells_per_art.sort_values(ascending=False)
    list_problem_arts = list(cells_per_art.index)
    df2 = df[df['Код \nноменклатуры'].isin(list_problem_arts)]
    print(df2.columns)
    print(len(df2))
    with pd.ExcelWriter('Товары которые нужно соединить общий.xlsx', engine='xlsxwriter') as writer:
        df2.sort_values('Код \nноменклатуры').to_excel(writer, index=False, na_rep='')
    df_tg = df2[df2['ТГ'] == tg]
    print(df_tg)
    with pd.ExcelWriter('Товары которые нужно соединить.xlsx', engine='xlsxwriter') as writer:
        df_tg.sort_values('Код \nноменклатуры').to_excel(writer, index=False, na_rep='')


if __name__ == '__main__':
    main()
