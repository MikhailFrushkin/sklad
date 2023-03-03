import re

import cv2
import pytesseract

from data.config import path


def read_image(img: str) -> list:
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=config, lang='eng')
    pattern = re.compile(r'\d{8}')
    result = re.findall(pattern, text)
    print(result)
    return result


if __name__ == '__main__':
    read_image(f'{path}/photos/test.jpg')
