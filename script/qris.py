import qrcode

data = "https://www.instagram.com/amadwoltemade?igsh=NHk3NWc1azd2bXRn"
qr = qrcode.make(data)
qr.save("qrcode.png")

print("qr berhasil dibuat!")