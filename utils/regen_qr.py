import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from data.config import path


def main():
    """Генерирует qr из списка qr_list
    box-size - качество qr 40 макс(долго регенит)"""
    qr_list = ['011_825-Exit_sklad', '011_825-Exit_Dost', '011_825-Exit_zal',
               '011_825-otkaz_sklad', 'R12_BrakIn_825', 'V-Sales_825']
    for data in qr_list:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=25)

        qr.add_data(data)
        img = qr.make_image(image_factory=StyledPilImage,
                            module_drawer=RoundedModuleDrawer(),
                            color_mask=RadialGradiantColorMask(
                                back_color=(255, 255, 255),
                                center_color=(255, 128, 0),
                                edge_color=(0, 0, 255)))
        img.save('{}/qcodes/{}.jpg'.format(path, data), 'JPEG')


if __name__ == '__main__':
    main()
