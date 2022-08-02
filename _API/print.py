from ctypes import alignment
from escpos.printer import Network

IP = "192.168.7.198"


def printer():
    payload = {
    "Asal" : "Alamat Asal",
    "Tujuan": "Alamat Tujuan",
    "Pengirim": "Nama Pengirim",
    "Penerima": "Nama Penerima",
    "No HP": "No Hp",
    "Berat" : "Kg",
    "Ongkir" : "0",
    "Diskon": "%",
    "Total Ongkir" : "Total"
    }

    logo = "D:/Si BOX/_API/logo.png"
    p = Network(IP)
    p.set(align = 'left')
    p.cut()
    p.image(logo, center = False)
    p.text('\n')
    p.text('\n')
    p.barcode('1234567890123', 'EAN13', 90, 3, '', '', align_ct = False)
    p.text('\n')
    p.text('\n')
    for key, value in payload.items():
        p.text(key, ': ', value)
    p.text('\n')
    p.cut()

printer()