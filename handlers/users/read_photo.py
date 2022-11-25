import cv2
import pytesseract

# Путь для подключения tesseract
from data.config import path

# data = pytesseract.image_to_data(img, config=config)
# # Перебираем данные про текстовые надписи
# for i, el in enumerate(data.splitlines()):
#     if i == 0:
#         continue
#
#     el = el.split()
#     try:
#         # Создаем подписи на картинке
#         x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
#         cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
#         cv2.putText(img, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
#     except IndexError:
#         print("Операция была пропущена")
#
# # Отображаем фото
# cv2.imshow('Result', img)
# cv2.waitKey(0)


def get_codes(file):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    img = cv2.imread('{}/files/photo_2022-11-23_23-23-27.jpg'.format(path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    config = r'--oem 3 --psm 6'
    print(pytesseract.image_to_string(img, config=config))


if __name__ == '__main__':
    get_codes(1)

