import re

import cv2
import pytesseract
import numpy as np

import matplotlib.pyplot as plt
from PIL import Image
from data.config import path


def read_image(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=config)
    pattern = re.compile(r'\d{8}')
    result = re.findall(pattern, text)
    print(result)


if __name__ == '__main__':
    read_image(f'{path}/photos/test.jpg')
