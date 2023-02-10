from pyzbar import pyzbar
import cv2


def draw_barcode(decoded, image):
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                          (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                          color=(0, 255, 0),
                          thickness=5)
    return image


def decode(image):
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        image = draw_barcode(obj, image)
        print(f"Data:{obj.data} {str(obj.data)[2:-1]}")
    return image


if __name__ == "__main__":
    from glob import glob

    barcodes = glob("*.png")
    for barcode_file in barcodes:
        print(barcode_file)
        img = cv2.imread(barcode_file)
        try:
            img = decode(img)
        except Exception as ex:
            print(ex, barcode_file)

