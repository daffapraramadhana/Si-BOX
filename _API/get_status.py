#GET STATUS DOOR
from flask import jsonify
import requests
import pandas as pd
import json
import sqlite3

url = 'http://192.168.0.10:8090/nlc02api'


def doorStatus(parameter):
    if parameter is None:
        pass
    else:
        door_stat1 = {'cmd': 'doorstat', 'bus': 1}
        door_stat2 = {'cmd': 'doorstat', 'bus': 2}
        r1 = requests.post(url, json = door_stat1)
        r2 = requests.post(url, json = door_stat2)

        if r1.ok and r2.ok:
            r1.text
            r2.text
            data1 = json.loads(r1.text)
            data2 = json.loads(r2.text)
            df = pd.DataFrame(data1, data2)

conn = sqlite3.connect("door.db")
c = conn.cursor()

df.to_sql("door_status",conn)
          

def modStatus(parameter):
    if parameter is None:
        pass
    else:
        mod_stat = {'cmd': 'modstat', 'bus': 0}
        r = requests.post(url, json = mod_stat)

        if r.ok:
            r.text
            stat = json.loads(r.text)
            return jsonify(stat)


