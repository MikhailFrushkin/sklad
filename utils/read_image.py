import re
import time

import cv2
import pytesseract
from PIL import Image
from data.config import path
from loader import bot


def read_image(img: str) -> list:
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=config, lang='eng')
    pattern = re.compile(r'\d{8}')
    result = re.findall(pattern, text)
    return result


def rotate_image(message, img):
    image = cv2.imread(img)
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, 90, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    cv2.imwrite(f'{path}/photos/фото_90_{message.from_user.id}.png', rotated)
    return rotated



if __name__ == '__main__':
    # read_image(f'{path}/photos/test2.jpg')
    rotate_image(f'{path}/photos/test2.jpg')
