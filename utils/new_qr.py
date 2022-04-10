import qrcode


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('V-Sales_825')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save('V-Sales_825.jpg', 'JPEG')
