from ctypes import alignment
from escpos.printer import Network
from PIL import Image
from datetime import datetime

def printer(data):
    payload = {
    "No Resi" : data['no_resi'],
    "Asal" : data['asal'],
    "Tujuan": data['tujuan'],
    "Pengirim": data['pengirim'],
    "Penerima": data['penerima'],
    "No HP": data['no_hp'],
    "Berat" : data['berat'],
    "Ongkir" : data['ongkir'],
    "Terminal ID" : data['terminal_id'],
    "Diskon": data['diskon'],
    "Total Ongkir" : data['total'],
    }
    IP = data['ip']
    # print (IP)
    merchant = data['merchant']
    # print(merchant)
    app = data['app_vers']
    create_date = datetime.now()
    info_date = create_date.strftime("%Y-%m-%d %H:%M") + " " + app
    logo = Image.open("C:/Si-BOX/_API/logo.png")
    new_logo = logo.resize((300,200))
    p = Network(IP)
    p.set(align = 'center')
    p.image(new_logo, center = True)
    p.text(merchant)
    p.text('------------------------------')
    p.text('\n')
    p.barcode(payload['No Resi'], 'EAN13', 90, 3, '', '', align_ct = True)
    p.text('\n')
    p.set(align = 'left')
    for key, value in payload.items():
        load = key + "       : " + value + '\n'
        p.text(f"{load}")
    p.text('\n')
    p.text('\n')
    p.text(info_date)
    p.cut()

# printer()