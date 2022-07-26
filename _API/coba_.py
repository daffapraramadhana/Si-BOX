import requests
import json
import time

url = 'http://192.168.0.10:8090/nlc02api'


def door(parameter):
    if parameter is None:
        print('Missing Parameter')
    else:
        door_open = {'cmd': 'open', 'door': None }
        door_open['door'] = parameter
        print(door_open)
        #r = requests.post(url, json = door_open)

for i in range (32) :
    door(i)
    time.sleep(2)

