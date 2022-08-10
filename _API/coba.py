
def check_data(data):
    data = data
    check = {
        "ip" : "",
        "no_resi" : "",
        "asal" : "",
        "tujuan": "",
        "pengirim": "",
        "penerima": "",
        "no_hp": "",
        "berat" : "",
        "ongkir" : "",
        "diskon": "",
        "total" : "",
        "merchant" : "",
        "app_vers" : ""
    }
    if all ( key in data for key in check):
        print("all data exist")
    else:
        return ("error")

data = {
        # "ip": "124",
        "no_resi" : "123456890",
        "asal" : "CGK",
        "tujuan": "Semarang, SRG",
        "pengirim": "tejo",
        "penerima": "surti",
        "no_hp": "098765",
        "berat" : "5 kg",
        "ongkir" : "35.000",
        "diskon": "0",
        "total" : "35.000",
        "merchant" : "JKT17, Kuningan City Lt. 3",
        "app_vers" : "app 1.0 Beta."
    }

def coba():
        a = check_data(data)
        if a  == 'error':
            print("error")

  
    
coba()
