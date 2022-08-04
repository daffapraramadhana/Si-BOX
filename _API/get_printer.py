from turtle import right
from escpos.printer import Network
from PIL import Image
from datetime import datetime

def printer(data):
    # payload = {
    # "Asal      ": data['asal'],
    # "Tujuan    ": data['tujuan'],
    # "Pengirim  ": data['pengirim'],
    # "Penerima  ": data['penerima'],
    # "No HP     ": data['no_hp'],
    # "Berat     ": data['berat'],
    # "Ongkir    ": data['ongkir'],
    # "Diskon    ": data['diskon'],
    # "Total Ongkir  ": data['total'],
    # }
    IP = data['ip']
    merchant = data['merchant']
    app = data['app_vers']
    create_date = datetime.now()
    info_date = create_date.strftime("%Y-%m-%d %H:%M") + ", " + merchant + "\n"
    logo = Image.open("C:/Si-BOX/_API/logo.png")
    new_logo = logo.resize((250,50))
    p = Network(f"{IP}")
    if p.ok :
        p.set(align = 'left')
        p.image(new_logo)
        p.text('\n')
        p.text('\n')
        gen_bar = data['no-resi']
        p.barcode(f"{gen_bar}", 'EAN13', 90, 3, '', '', align_ct = False)
        p.text('\n')
        p.set(align = 'left')
        resi = "No Resi :  " + data['no_resi'] + "\n"
        p.text(f"{resi}")
        p.text("  \n")
        asal     = "Asal      :  " + data['asal'] + "\n"
        tujuan   = "Tujuan    :  " + data['tujuan'] + "\n"
        pengirim = "Pengirim  :  " + data['pengirim'] + "\n"
        penerima = "Penerima  :  " + data['penerima'] + "\n"
        no_hp    = "No HP     :  " + data['no_hp'] + "\n"
        berat    = "Berat     :  " + data['berat'] + "\n"
        ongkir   = "Ongkir    :  " + data['ongkir'] + "\n"
        diskon   = "Diskon    :  " + data['diskon'] + "\n"
        total    = "Total Ongkir : " + data['ongkir'] + "\n"
        p.text(f"{asal}")
        p.text(f"{tujuan}")
        p.text(f"{pengirim}")
        p.text(f"{penerima}")
        p.text(f"{no_hp}")
        p.text(f"{berat}")
        p.text(f"{ongkir}")
        p.text(f"{diskon}")
        p.text(f"{total}")
        p.text('\n')
        p.text('\n')
        p.set(align='center')
        p.text(info_date)
        p.set(align=right)
        p.text(f"{app}")
        p.cut()

    

# printer()