import re
import time

import cv2
import pytesseract
from PIL import Image
from data.config import path
import numpy as np
from loader import bot


def read_image(img: str) -> list:
    img = cv2.imread(img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    for angle in [0, 270, 90, 180, 45, 135, 315]:
        (h, w) = img.shape[:2]
        center = (w / 2, h / 2)

        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))
        cv2.imwrite(f'{path}/photos/фото_{angle}.png', rotated)

        config = r'--oem 1 --psm 6'
        text = pytesseract.image_to_string(rotated, config=config, lang='eng')

        pattern = re.compile(r"\b\d{8}\b")
        result = re.findall(pattern, text)

        if result:
            print(result)
        else:
            hsv_img = cv2.cvtColor(rotated, cv2.COLOR_BGR2HSV)
            # определите диапазон красного цвета в HSV
            lower_red = np.array([0, 50, 50])
            upper_red = np.array([10, 255, 255])
            mask1 = cv2.inRange(hsv_img, lower_red, upper_red)
            lower_red = np.array([170, 50, 50])
            upper_red = np.array([180, 255, 255])
            mask2 = cv2.inRange(hsv_img, lower_red, upper_red)

            # Объединить две маски красного цвета в одну
            mask = mask1 + mask2
            masked_img = cv2.bitwise_and(rotated, rotated, mask=mask)
            red_text = cv2.cvtColor(masked_img, cv2.COLOR_HSV2BGR)
            cv2.imwrite(f'result{angle}.png', red_text)
            text = pytesseract.image_to_string(red_text, config=config, lang='eng')
            pattern = re.compile(r"\b\d{8}\b")
            result = re.findall(pattern, text)
            if len(result) != 0:
                return result
            print("Совпадений не найдено.")
        if len(result) != 0:
            return result


if __name__ == '__main__':
    read_image(f'{path}/photos/test3.jpg')
