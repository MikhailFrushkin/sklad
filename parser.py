from bs4 import BeautifulSoup

with open('Hoff.html', 'rb') as file:
    crs = file.read()
    # print(crs)

soup = BeautifulSoup(crs, 'lxml')

# title = soup.title
# print(title.string)
menu = soup.find(class_='c-input__container')
print(menu)

# all_a = soup.find_all('a')
# for i in all_a:
#     i_text = i.text
#     i_url = i.get('href')
#     print('{}:{}'.format(i_text, i_url))